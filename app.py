from flask import Flask, render_template, request, jsonify
import sqlite3 # import database
app = Flask(__name__)
def init_db():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (    id INTEGER PRIMARY KEY AUTOINCREMENT,user_message TEXT, bot_reply TEXT)""")
    conn.commit()
    conn.close()
init_db()
last_topic = "" # memory
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/chat", methods=["POST"])
def chat():
    global last_topic
    user_message = request.json["message"].lower()
    if "hello" in user_message or "hi" in user_message:
        reply = "Hello 👋 Welcome to BS Market AI"
    elif "vanakkam" in user_message:
        reply = "Vanakkam 👋 BS Market AI ungaalai varaverkirathu!"
    elif "வணக்கம்" in user_message:
        # Tamil input → Tanglish output
        reply = "Vanakkam 👋 BS Market AI ungaalai varaverkirathu!"
    elif "service pathi sollu" in user_message or "services pathi sollu" in user_message:
        last_topic = "service"
        reply = "Naanga Digital Marketing, Website Development, SEO, Branding and AI Services panrom."
    elif "service" in user_message:
        last_topic = "service"
        reply = "We provide Digital Marketing, Website Development, SEO, Branding and AI Services."
    elif "சர்வீஸ்" in user_message or "சேவை" in user_message or "சர்வீசஸ்" in user_message: # Tamil input → Tanglish output
        last_topic = "service"
        reply = "Naanga Digital Marketing, Website Development, SEO, Branding and AI Services panrom."
    elif "marketing pathi sollu" in user_message:
        last_topic = "marketing"
        reply = "Naanga Social Media Marketing, Instagram Promotion and Business Ads panrom."
    elif "marketing" in user_message:
        last_topic = "marketing"
        reply = "We provide Social Media Marketing, Instagram Promotion and Business Ads."
    elif "மார்க்கெட்டிங்" in user_message:
        last_topic = "marketing"
        reply = "Naanga Social Media Marketing, Instagram Promotion and Business Ads panrom."
    elif "package pathi sollu" in user_message or "packages pathi sollu" in user_message:
        last_topic = "package"
        reply = "Engakitta Basic, Premium and Advanced Packages irukku."
    elif "package" in user_message or "packages" in user_message:
        last_topic = "package"
        reply = "We have Basic, Premium and Advanced Packages."
    elif "பேக்கேஜ்" in user_message or "பேக்கேஜை" in user_message:
        last_topic = "package"
        reply = "Engakitta Basic, Premium and Advanced Packages iruku"
    elif "seo pathi sollu" in user_message:
        last_topic = "seo"
        reply = "Naanga SEO Optimization and Google Ranking panrom."
    elif "seo" in user_message:
        last_topic = "seo"
        reply = "We provide SEO Optimization, Google Ranking and Keyword Marketing."
    elif "எஸ்இஓ" in user_message:
        last_topic = "seo"
        reply = "Naanga SEO Optimization and Google Ranking panrom."
    elif "location pathi sollu" in user_message:
        last_topic = "location"
        reply = "Naanga Tamil Nadu full ah and online la services panrom."
    elif "location" in user_message or "where" in user_message:
        last_topic = "location"
        reply = "We provide services all over Tamil Nadu and Online."
    elif "லொகேஷன்" in user_message or "எங்கே" in user_message:
        last_topic = "location"
        reply = "Naanga Tamil Nadu full ah and online la services panrom."
    elif "order pathi sollu" in user_message:
        last_topic = "order"
        reply = "Neenga WhatsApp moolama order place panna mudiyum."
    elif "order" in user_message:
        last_topic = "order"
        reply = "You can place your orders through WhatsApp or direct contact."
    elif "ஆர்டர்" in user_message:
        last_topic = "order"
        reply = "Neenga WhatsApp moolama order place panna mudiyum."
# pure tamil
    elif "தமிழில் சொல்லு" in user_message or "தமிழ்ல சொல்லு" in user_message or "தமிழிலேயே சொல்லு" in user_message:
        if last_topic == "service":
            reply = "நாங்கள் டிஜிட்டல் மார்க்கெட்டிங், வெப்சைட் டெவலப்மென்ட், SEO, Branding மற்றும் AI Services செய்கிறோம்."
        elif last_topic == "marketing":
            reply = "நாங்கள் Social Media Marketing, Instagram Promotion மற்றும் Business Ads செய்கிறோம்."
        elif last_topic == "package":
            reply = "எங்களிடம் Basic, Premium மற்றும் Advanced Packages உள்ளது."
        elif last_topic == "seo":
            reply = "நாங்கள் SEO Optimization மற்றும் Google Ranking செய்கிறோம்."
        elif last_topic == "location":
            reply = "நாங்கள் தமிழ்நாடு முழுவதும் மற்றும் ஆன்லைனில் சேவைகள் செய்கிறோம்."
        elif last_topic == "order":
            reply = "நீங்கள் WhatsApp மூலம் order செய்யலாம்."
        else:
            reply = "எதை தமிழில் சொல்ல வேண்டும்?"
    else:
        reply = "Sorry 😅 Enakku puriyala."
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chats (user_message, bot_reply) VALUES (?, ?)",
        (user_message, reply)
    )
    conn.commit()
    conn.close()
    # RETURN RESPONSE
    return jsonify({
        "reply": reply
    })
@app.route("/chats")
def view_chats():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chats")
    chats = cursor.fetchall()
    conn.close()
    html =   """ <h1>Chat History</h1>
    <table border='1' cellpadding='10'>
        <tr>
            <th>ID</th>
            <th>User Message</th>
            <th>Bot Reply</th>
        </tr>"""
    for chat in chats:
        html += f"""
        <tr>
            <td>{chat[0]}</td>
            <td>{chat[1]}</td>
            <td>{chat[2]}</td>
        </tr>
        """
    html += "</table>"
    return html
if __name__ == "__main__":
    app.run(debug=True)