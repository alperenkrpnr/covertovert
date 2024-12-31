from CovertChannelBase import CovertChannelBase
import time
import random
from scapy.all import sniff, LLC, Raw, IP, UDP

class MyCovertChannel(CovertChannelBase):
    """
    - You are not allowed to change the file name and class name.
    - You can edit the class in any way you want (e.g. adding helper functions); however, there must be a "send" and a "receive" function, the covert channel will be triggered by calling these functions.
    """
    def __init__(self):
        """
        - You can edit __init__.
        """
        super().__init__()

    def send(self, log_file_name, parameter1, parameter2):
        """
        - In this function, you expected to create a random message (using function/s in CovertChannelBase), and send it to the receiver container. Entire sending operations should be handled in this function.
        - After the implementation, please rewrite this comment part to explain your code basically.
        """
        binary_message = self.generate_random_binary_message_with_logging(log_file_name, min_length=16, max_length=16)

        start_time = time.perf_counter()

        for bit in binary_message:
            packets_in_burst = random.randint(1, 3)
            
            for _ in range(packets_in_burst):
                # Send the packets
                packet = IP(dst="172.18.0.3") / UDP(dport=1234, sport=4321)
                super().send(packet)

            # Wait for the appropriate idle period based on the bit
            if bit == '0':
                time.sleep(parameter1 / 1000)  # Convert to seconds
            elif bit == '1':
                time.sleep(parameter2 / 1000)
        super().send(packet)

        end_time = time.perf_counter()

        # calculate total time
        total_time = end_time - start_time

        print(f"Total time to send the message: {total_time:.4f} seconds")

        # calculate covert channel capacity
        capacity = 128 / total_time
        print(f"Covert Channel Capacity: {capacity:.2f} bits per second")
        

    def receive(self, parameter1, parameter2, parameter3, burst_time_threshold, log_file_name):
        """
        Receiver fonksiyonu:
        - Her paket arasındaki süreyi ölçer.
        - Eğer iki paket arasındaki süre burst_time_threshold'dan küçük veya eşitse, burst içindeyizdir ve hiçbir işlem yapılmaz.
        - Eğer iki paket arasındaki süre burst_time_threshold'dan büyükse, idle'dayızdır ve parameter3 ile kıyaslama yapılarak mesaj çözülür.
        """
        start_time = None
        binary_message = ""
        decoded_message = ""
        
        def packet_callback(packet):
            nonlocal start_time, binary_message, decoded_message
            current_time = time.perf_counter()

            if start_time is not None:
                packet_interval = (current_time - start_time) * 1000  # Convert to milliseconds
            
                if packet_interval > burst_time_threshold:
                    # we are in idle
                    if packet_interval < parameter3:
                        binary_message += '0'
                        print(f'Packet interval: {packet_interval:.2f} ms')

                    else:
                        binary_message += '1'
                        print(f'Packet interval: {packet_interval:.2f} ms')

                    if len(binary_message) >= 8:
                        if binary_message[:8] == "00100000":
                            decoded_message += " "  # add space character to the decoded message
                            
                        else:
                            char = self.convert_eight_bits_to_character(binary_message[:8])
                            decoded_message += char

                        # remove the converted bits
                        binary_message = binary_message[8:]

                else:
                    # we are in burst, do nothing
                    pass

            # update the start time
            start_time = current_time

        # Sniff packets until the termination character is detected
        sniff(filter="udp and dst port 1234", prn=packet_callback, stop_filter=lambda x: "." in decoded_message)

        # Convert binary message back to string
        super().log_message(decoded_message, log_file_name)
