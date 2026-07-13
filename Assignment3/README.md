# The Multiverse of Chatbots 🌌

An upgraded, professional version of the "Multiverse of Chatbots" Streamlit app —
now with 9 personalities, a live-typing effect, chat memory per persona, and
real replies powered by the Gemini API.

## What's new vs. the original

- **9 personas** instead of 3 (hacker, angry Ravi Shastri, Ronaldo fan, Yoda,
  sarcastic teenager, Gordon Ramsay, Shakespearean poet, motivational coach, pirate)
- **Real chat UI** using `st.chat_message` / `st.chat_input` with avatars
- **Live "typing" effect** — replies appear letter by letter, like a real chat
- **Separate conversation memory** for each persona
- **Polished, professional dark theme** with gradient title and status indicators
- **Clear error handling** if the API key is missing or a request fails
- **`.env` support** so your API key never lives in the code

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

## 2. Add your Gemini API key

Open the `.env` file in this folder and paste your key:

```
GEMINI_API_KEY=your_actual_key_here
```

Get a free key at: https://aistudio.google.com/apikey

## 3. Run the app

```bash
streamlit run app.py
```

Your browser will open at `http://localhost:8501`.

## 4. Use it

1. Pick a personality from the sidebar.
2. Type a message in the chat box at the bottom.
3. Watch the reply type itself out in real time.
4. Switch personas anytime — each one remembers its own conversation.
5. Use "Clear this conversation" in the sidebar to reset a persona's memory.
## Chat history behavior

- Each persona keeps its own chat history during the current Streamlit session.
- The history is stored in browser session state and is not saved permanently to a file.
- Refreshing the page, restarting the app, or clicking "Clear this conversation" will reset that persona's history.
## Notes

- If you see "Missing key" in the sidebar, double-check your `.env` file is saved
  and restart `streamlit run app.py`.
- You can change the model by uncommenting `GEMINI_MODEL` in `.env` (e.g. to a
  faster or more powerful Gemini model if you have access).
- Never commit your `.env` file with a real key to a public GitHub repo.
