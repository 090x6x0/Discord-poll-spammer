import requests, random, threading, time
from itertools import cycle

tokens = open('tokens.txt', 'r').read().splitlines()

class poll_spammer():
    @staticmethod
    def gen_nonce():
        return ''.join(str(random.randint(0, 9)) for _ in range(19))
    
    @staticmethod
    def get_cookies():
        response = requests.get("https://discord.com/api/v9/experiments")
        if response.status_code == 200:
            cookies = response.cookies.get_dict()
            return "; ".join([f"{key}={value}" for key, value in cookies.items()])
        else:
            print(f"Failed to fetch cookies > {response.text}")
            return ""

    @staticmethod
    def poll_spam(token, nonce, cookies, chan, mess):
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "cs,en-US;q=0.9",
            "authorization": token,
            "content-type": "application/json",
            "cookie": cookies,
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9175 Chrome/128.0.6613.186 Electron/32.2.7 Safari/537.36",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MTc1Iiwib3NfdmVyc2lvbiI6IjEwLjAuMjI2MzEiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJ4NjQiLCJzeXN0ZW1fbG9jYWxlIjoiY3MiLCJoYXNfY2xpZW50X21vZHMiOmZhbHNlLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBkaXNjb3JkLzEuMC45MTc1IENocm9tZS8xMjguMC42NjEzLjE4NiBFbGVjdHJvbi8zMi4yLjcgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjMyLjIuNyIsIm9zX3Nka192ZXJzaW9uIjoiMjI2MzEiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjozNTU2MjQsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjU2NzE2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
        }

        payload = {
            "content": "",
            "flags": 0,
            "mobile_network_type": "unknown",
            "nonce": nonce,
            "poll": {
                "allow_multiselect": False,
                "question": {"text": mess},
                "answers": [
                    {"poll_media": {"text": mess}}
                ],
                "duration": 24
            },
            "layout_type": 1,
            "tts": False
        }

        try:
            response = requests.post(f"https://discord.com/api/v9/channels/{chan}/messages", headers=headers, json=payload)
            if response.status_code == 200:
                print(f"Poll successfully sent with token > {token[:35]}****")
            else:
                print(f"Failed to send poll. Status code > {response.status_code} Response > {response.text}")
        except requests.RequestException as e:
            print(f"Error while sending poll: {e}")

def spam_polls(chan, mess, delay, how_many_polls):
    poll_in = poll_spammer
    threads = []
    cl_tokens = []

    for token_ln in tokens:
        cl_tokens.append(token_ln.split(":")[-1] if ":" in token_ln else token_ln)

    tokens_cycle = cycle(cl_tokens)

    def send(token):
        nonce = poll_in.gen_nonce()
        cookies = poll_in.get_cookies()
        if cookies:
            poll_in.poll_spam(token, nonce, cookies, chan, mess)

    for _ in range(how_many_polls):
        token = next(tokens_cycle)
        thread = threading.Thread(target=send, args=(token,))
        threads.append(thread)
        thread.start()
        time.sleep(delay)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    try:
        chan = input("Channel ID > ")
        mess = input("Message > ")
        how_many_polls = int(input("How many polls to spam? > "))

        while True:
            print("Recommended delay is 0.5!")
            delay = float(input("Delay between polls (at least 0.4) > "))
            if delay >= 0.4:
                break
            else:
                print("Warning > You should use at least delay 0.4 to avoid CloudFlare Restrict!")

        spam_polls(chan, mess, delay, how_many_polls)
    except ValueError:
        print("Invalid input.")
    input("Press enter to exit...")