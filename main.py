
import os
import requests
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Custom class to store and display AI response
class AIResponse:

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def display(self):
        print("\n" + "=" * 50)
        print("             AI RESPONSE")
        print("=" * 50)

        print(f"\nQuestion:\n{self.question}")
        print(f"\nAnswer:\n{self.answer}")

        print("\n" + "=" * 50)


# Function to send question to Gemini API
def ask_ai(question):

    if not API_KEY:
        print("Error: API Key not found. Check your .env file.")
        return

    model = "gemini-3.5-flash-lite"

    url = (
        f"https://generativelanguage.googleapis.com/"
        f"v1beta/models/{model}:generateContent"
    )

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }

    # JSON request body
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": question}
                ]
            }
        ]
    }

    try:
        print("\nSending your question to Gemini AI...")

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        # Check HTTP status code
        response.raise_for_status()

        # Parse JSON response
        data = response.json()

        # Extract AI answer
        answer = data["candidates"][0]["content"]["parts"][0]["text"]

        # Create object and display result
        result = AIResponse(question, answer)
        result.display()

    except requests.exceptions.HTTPError:
        print("\nHTTP Error:", response.status_code)

        try:
            print(response.json())
        except ValueError:
            print(response.text)

    except requests.exceptions.Timeout:
        print("\nError: Request timed out. Please try again.")

    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API.")

    except (KeyError, IndexError, TypeError):
        print("\nError: Unexpected API response format.")
        print(response.text)

    except requests.exceptions.RequestException as error:
        print("\nRequest Error:", error)


# Main program
def main():

    print("=" * 50)
    print("       AI QUESTION ANSWERING SYSTEM")
    print("             Powered by Gemini")
    print("=" * 50)

    while True:

        question = input("\nEnter your question (or type 'exit' to quit): ")

        if question.lower().strip() == "exit":
            print("\nThank you for using the AI system!")
            break

        if not question.strip():
            print("Please enter a valid question.")
            continue

        ask_ai(question)


if __name__ == "__main__":
    main()
