import time
import base64

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QBuffer, QIODevice

class ImageReconstructor(QObject):
    image_reconstructed = pyqtSignal(QPixmap)
    avg_latency_updated = pyqtSignal(float, float, float)
    interval_between_loops_emitted = pyqtSignal(float)

    def __init__(self, mongo_handler, xor_key):
        super().__init__()
        self.mongo_handler = mongo_handler
        self.xor_key = xor_key
        self.chunks={}
        self.total_chunks = None
        self.last_image_timestamp = None

        self.cumulative_latency_esp_to_db = 0
        self.cumulative_latency_db_to_program = 0
        self.cumulative_latency_total = 0
        self.image_count = 0

    def decrypt_and_recombine(self):
        try:
            decrypted_image = b""
            sorted_chunks = sorted(self.chunks.values(), key=lambda x: x['chunk'])

            for chunk_data in sorted_chunks:
                print(f"Processing chunk: {chunk_data['chunk']}")
                encrypted_data = base64.b64decode(chunk_data['data'])
                print(f"Base64 decoded length: {len(encrypted_data)}")
                print(f"Encrypted data (hex): {encrypted_data.hex()[:50]}...")  # Print first 50 bytes

                # XOR decryption
                decrypted_chunk = bytes([byte ^ self.xor_key for byte in encrypted_data])
                print(f"Decrypted chunk length: {len(decrypted_chunk)}")
                print(f"Decrypted chunk (hex): {decrypted_chunk.hex()[:50]}...")  # Print first 50 bytes
                decrypted_image += decrypted_chunk

            buffer = QBuffer()
            buffer.open(QIODevice.WriteOnly)
            buffer.write(decrypted_image)
            buffer.close()

            pixmap = QPixmap()
            pixmap.loadFromData(buffer.data())

            if hasattr(self, 'image_reconstructed') and self.image_reconstructed is not None:
                print("Emitting image_reconstructed signal")
                self.image_reconstructed.emit(pixmap)
            else:
                print("Warning: image_reconstructed signal not properly set up.")

        except ValueError as e:
            print(f"Outer ValueError: {e}")
        except Exception as e:
            print(f"Error decrypting and recombining image: {e}")

    def process_new_document(self, document):
        chunk = document["chunk"]
        total_chunks = document["total_chunks"]
        timestamp_esp = document["timestamp_esp"]
        timestamp_mqtt = document["timestamp_mqtt"]
        timestamp_now = time.time()

        latency_esp_to_db = timestamp_mqtt - timestamp_esp
        latency_db_to_program = timestamp_now - timestamp_mqtt
        latency_total = timestamp_now - timestamp_esp

        self.cumulative_latency_esp_to_db += latency_esp_to_db
        self.cumulative_latency_db_to_program += latency_db_to_program
        self.cumulative_latency_total += latency_total
        self.image_count += 1

        avg_latency_esp_to_db = round(self.cumulative_latency_esp_to_db / self.image_count, 4)
        avg_latency_db_to_program = round(self.cumulative_latency_db_to_program / self.image_count, 4)
        avg_latency_total = round(self.cumulative_latency_total / self.image_count, 4)

        self.avg_latency_updated.emit(avg_latency_esp_to_db, avg_latency_db_to_program, avg_latency_total)

        self.chunks[chunk] = document
        self.total_chunks = total_chunks

        if len(self.chunks) == total_chunks:
            if self.last_image_timestamp:
                interval_between_loops = timestamp_esp - self.last_image_timestamp
                self.interval_between_loops_emitted.emit(interval_between_loops)
                print(f"Interval between loops: {interval_between_loops} seconds")
            self.last_image_timestamp = timestamp_esp
            print("All chunks received, decrypting and recombining image...")
            self.decrypt_and_recombine()
            self.chunks.clear()
