# Covert Timing Channel that exploits Idle Period Between Packet Bursts using IP [Code: CTC-IPPB-IP]

Explain your study in detail as you share your work with the community in a public repository. Anyone should understand your project when read it without having a previous information about the homework.

# Covert Timing Channel Implementation

This project implements a covert timing channel using packet bursts and idle times to encode and transmit binary messages between a sender and a receiver. The project is structured to allow the calculation of covert channel capacity and provides explanations for parameter choices and limitations.

---

## Overview

In this implementation:
- **Sender** encodes a binary message into packet bursts with idle times between them.
- **Receiver** decodes the message by analyzing idle times between received packets.
- The covert channel capacity is calculated as the number of bits transmitted per second.

The system adheres to the requirements of the assignment, providing a complete implementation of the covert timing channel.

---

## Components

### Sender
The sender creates a random binary message and transmits it using packet bursts with controlled idle times. Key steps include:
1. **Binary Message Generation**: A binary message of 128 bits (16 characters) is generated using the `generate_random_binary_message_with_logging` function.
2. **Packet Burst Transmission**: For each bit, a burst of packets is sent. The number of packets per burst is randomly chosen between 1 and 3 to prevent predictability.
3. **Idle Time Control**:
   - A `0` bit is represented by an idle time of `parameter1` milliseconds.
   - A `1` bit is represented by an idle time of `parameter2` milliseconds.
4. **Timing and Capacity Calculation**:
   - The transmission time is measured using `time.perf_counter`.
   - The covert channel capacity is calculated as:

     \[
     \text{Capacity} = \frac{128}{\text{Transmission Time (seconds)}} \text{ bits/second}
     \]
     \text{and we found it as 2.32 bits/second}

### Receiver
The receiver decodes the binary message by analyzing idle times between packet arrivals. Key steps include:
1. **Packet Sniffing**: Packets are sniffed on the designated port.
2. **Idle Time Analysis**:
   - Idle times greater than `burst_time_threshold` are analyzed:
     - If the idle time is less than `parameter3`, it is decoded as `0`.
     - Otherwise, it is decoded as `1`.
   - Idle times less than or equal to `burst_time_threshold` are ignored as part of bursts.
3. **Binary to Character Conversion**:
   - The binary message is processed in chunks of 8 bits to form ASCII characters.
   - The special case of `00100000` (space character) is handled explicitly.

---

## Parameters and Configuration

The parameters are defined in `config.json` and are explained below:

### Sender Parameters
| Parameter    | Value | Description                                                                 |
|--------------|-------|-----------------------------------------------------------------------------|
| `parameter1` | 170ms | Idle time for `0` bits, chosen to ensure clear differentiation from `1`.     |
| `parameter2` | 610ms | Idle time for `1` bits, chosen to ensure clear differentiation from `0`.     |
| `log_file_name` | `Sender.log` | Log file for the generated binary message.                                |

### Receiver Parameters
| Parameter             | Value  | Description                                                                 |
|-----------------------|--------|-----------------------------------------------------------------------------|
| `parameter1`          | 170ms  | Matches the sender's `parameter1`.                                          |
| `parameter2`          | 610ms  | Matches the sender's `parameter2`.                                          |
| `parameter3`          | 385ms  | Threshold for differentiating `0` and `1` based on idle time.               |
| `burst_time_threshold`| 185ms  | Maximum interval between packets in a burst to prevent misclassification.    |
| `log_file_name`       | `Receiver.log` | Log file for the decoded binary message.                                   |

#### Parameter Choice Explanation
- **Idle Times (`parameter1`, `parameter2`)**: Chosen to maximize the differentiation between `0` and `1` while minimizing transmission errors due to network jitter.
- **`parameter3`**: Set as the midpoint of `parameter1` and `parameter2` to serve as a threshold for distinguishing `0` and `1`.
- **`burst_time_threshold`**: Selected to avoid classifying burst intervals as idle times. A higher value might misclassify bursts as idle times.

---

## Covert Channel Capacity

The covert channel capacity is calculated by dividing the length of the binary message (128 bits) by the total transmission time (in seconds):

\[
\text{Capacity} = \frac{128}{\text{Transmission Time (seconds)}} \text{ bits/second}
\]

For example, if the transmission time is 14.26 seconds, the capacity is:
\[
\text{Capacity} = \frac{128}{14.26} \approx 8.98 \text{ bits/second}
\]

This result is printed to the console and can also be logged in the `README.md` file.

---

## Limitations

1. **Parameter Limits**:
   - `parameter1` and `parameter2` must have sufficient differentiation to prevent misclassification of `0` and `1` bits.
   - `burst_time_threshold` must be carefully set to avoid false idle time detections.

2. **Network Conditions**:
   - High jitter or packet loss in the network can affect the accuracy of idle time measurements and degrade performance.

3. **Capacity Dependence**:
   - The covert channel capacity is inversely proportional to the idle times and total transmission time. Longer idle times reduce capacity but improve accuracy.

---

## Usage Instructions

1. **Sender Execution**:
   - Run the `send` function with the parameters defined in `config.json`.
   - The binary message will be logged in `Sender.log`, and the capacity will be printed to the console.

2. **Receiver Execution**:
   - Run the `receive` function with the parameters defined in `config.json`.
   - The decoded message will be logged in `Receiver.log`.

3. **Covert Channel Capacity**:
   - The capacity is calculated during the `send` execution and printed to the console.

---

## Conclusion

This implementation successfully demonstrates a covert timing channel by encoding binary messages into packet bursts and idle times. It provides a practical example of how timing channels can be utilized for covert communication, along with considerations for parameter tuning and limitations.
