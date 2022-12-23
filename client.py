import sys
import asyncio

from config import ENCODING, PROTOCOL, PHONES_LIMIT


async def main():
    try:
        _, address, port, *_ = sys.argv
    except Exception:
        raise Exception("Не введен адрес и порт")
    port = int(port)
    verb = input("Enter request type:\n")
    if verb not in ("ОТДОВАЙ", "ЗОПИШИ", "УДОЛИ"):
        raise Exception("Undefined method")
    name = input("Enter the name:\n")
    if not name:
        raise Exception("Name is not entered")
    message = " ".join((verb, name, PROTOCOL))
    if verb == "ЗОПИШИ":
        phones = []
        print("Enter phones below, type 'q' to quit:\n")
        for i in range(1, PHONES_LIMIT + 1):
            phone = input(f"Phone number {i}: ")
            if phone == "q":
                break
            phones.append(phone)
        message = "\r\n".join((message, *phones))
    message += "\r\n\r\n"
    message_encoded = message.encode(ENCODING)
    print(
            "-------------------------------\n" \
            f"REQUESTED TO: {address, port}\n" \
            f"DECODED: {message.strip()}\n" \
            "-------------------------------\n")

    reader, writer = await asyncio.open_connection(address, port)

    writer.write(message_encoded)
    await writer.drain()

    response = b""
    while True:
        line = await reader.readline()
        response += line
        if response.endswith(b"\r\n\r\n") or not line:
            break

    decoded_response = response.decode(ENCODING)
    addr = writer.get_extra_info("peername")
    print(
            "-------------------------------\n" \
            f"RECEIVED FROM SERVER: {addr}\n" \
            f"DECODED: {decoded_response.strip()}\n"\
            "-------------------------------\n")

    print("Close the connection")
    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as err:
        print(err)