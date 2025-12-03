from google import genai
import os

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("No GEMINI_API_KEY found in environment variables.")
        return

    client = genai.Client(api_key=api_key)

    model_name = "gemini-3-pro-preview"  # safe + free tier friendly

    response = client.models.generate_content(
        model=model_name,
        contents="Say hello in a fancy way."
    )

    print("Gemini Response:")
    print(response.text)


if __name__ == "__main__":
    main()
