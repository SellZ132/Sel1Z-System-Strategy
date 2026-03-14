import os
import discord
from discord.ext import commands, tasks
from discord import ui
from flask import Flask
from threading import Thread
import datetime

# --- ส่วนระบบหลอก Port (คงไว้เพื่อให้ Railway แสดงสถานะ Web) ---
app = Flask('')
@app.route('/')
def home():
    return "Sel1Z Bot is Online & Monitoring!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

TOKEN = os.getenv('DISCORD_TOKEN')

# --- ตั้งค่าสิทธิ์บอท ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- 1. Persistent Download View (ปุ่มอมตะ) ---
# เราต้องตั้ง timeout=None และใส่ custom_id เพื่อให้บอทจำปุ่มได้ตลอดไป
class DownloadView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
        self.add_item(ui.Button(
            label="Download .bat", 
            url="https://github.com/SellZ132/Sel1Z_System-Strategy/releases/download/v2.4/Sel1Z_Optimizer.bat", 
            emoji="📥",
            style=discord.ButtonStyle.link,
            custom_id="persistent_download_btn" # ID สำคัญสำหรับการจำ
        ))
        
        self.add_item(ui.Button(
            label="GitHub Repository", 
            url="https://github.com/SellZ132/Sel1Z-System-Strategy", 
            emoji="⭐",
            style=discord.ButtonStyle.link,
            custom_id="persistent_github_btn"
        ))

    async def callback(self, interaction: discord.Interaction):
        # ข้อมูลแบบละเอียด เน้นผลลัพธ์ ไม่เน้นคำสั่ง
        responses = {
            "th": (
                "🛡️ **[ Sel1Z SYSTEM STRATEGY v2.4 ]**\n\n"
                "**🚀 รายละเอียดการปรับแต่งระบบ:**\n"
                "• **การจัดการไฟล์ขยะเชิงลึก:** ทำความสะอาดไฟล์ตกค้างจากระบบปฏิบัติการและแคชของ Windows Update เพื่อเพิ่มพื้นที่ว่างและลดภาระการทำงานของ Disk\n"
                "• **การตรวจสอบเสถียรภาพ:** วิเคราะห์และซ่อมแซมความผิดปกติของไฟล์ระบบโดยรวม เพื่อป้องกันปัญหาเครื่องค้างหรือ Blue Screen ในระยะยาว\n"
                "• **การปรับแต่งเครือข่ายขั้นสูง:** รีเซ็ตโครงสร้างการเชื่อมต่อใหม่ทั้งหมดเพื่อลดค่า Latency และแก้ปัญหาอาการปิงแกว่งขณะเล่นเกมออนไลน์\n"
                "• **Gaming Mode (Optimization):** ยุติการทำงานของเซอร์วิสเบื้องหลังที่ไม่จำเป็นชั่วคราว เพื่อดึงทรัพยากร CPU และ RAM มาใช้กับตัวเกมอย่างเต็มประสิทธิภาพ\n\n"
                "⚠️ **ข้อควรระวังสำคัญ:**\n"
                "1. อินเทอร์เน็ตจะตัดการเชื่อมต่อและรีเซ็ตใหม่ครู่หนึ่ง\n"
                "2. ระบบการพิมพ์ (Printer) จะถูกปิดใช้งานจนกว่าจะรีสตาร์ทเครื่อง\n"
                "3. **ต้องรันด้วยสิทธิ์ Administrator เท่านั้นเพื่อให้ระบบทำงานได้สมบูรณ์**"
            ),
            "en": (
                "🛡️ **[ Sel1Z SYSTEM STRATEGY v2.4 ]**\n\n"
                "**🚀 Optimization Overview:**\n"
                "• **Advanced Junk Elimination:** Purges deep-seated system debris and Windows Update cache to maximize storage efficiency and disk response time.\n"
                "• **System Integrity Check:** Scans and restores core system components to ensure maximum OS stability and prevent unexpected crashes.\n"
                "• **Network Recalibration:** Full reset of the network stack to minimize latency, reduce jitter, and stabilize ping for competitive gaming.\n"
                "• **Gaming Mode Engagement:** Temporarily suspends non-essential background telemetry and services, prioritizing CPU/RAM for the active gaming environment.\n\n"
                "⚠️ **Crucial Warnings:**\n"
                "1. Your network connection will reset briefly during the process.\n"
                "2. Printing services will be disabled until the next system reboot.\n"
                "3. **Run as Administrator is mandatory for full execution.**"
            ),
            "de": (
                "🛡️ **[ Sel1Z SYSTEM STRATEGY v2.4 ]**\n\n"
                "**🚀 Optimierungsdetails:**\n"
                "• **Tiefenreinigung:** Entfernt tief im System liegende Dateireste und den Windows Update-Cache für maximale Effizienz.\n"
                "• **Systemstabilität:** Analysiert und repariert wichtige Systemkomponenten, um Betriebssystemfehler zu vermeiden.\n"
                "• **Netzwerkkalibrierung:** Vollständiger Reset des Netzwerk-Stacks zur Minimierung von Latenz und Ping-Schwankungen.\n"
                "• **Gaming-Modus:** Deaktiviert vorübergehend unnötige Hintergrunddienste, um CPU und RAM für Spiele zu maximieren.\n\n"
                "⚠️ **Wichtige Hinweise:**\n"
                "1. Die Internetverbindung wird kurzzeitig unterbrochen.\n"
                "2. Druckdienste sind bis zum nächsten Neustart deaktiviert.\n"
                "3. **Muss als Administrator ausgeführt werden.**"
            ),
            "ru": (
                "🛡️ **[ Sel1Z SYSTEM STRATEGY v2.4 ]**\n\n"
                "**🚀 Обзор оптимизации:**\n"
                "• **Глубокая очистка:** Удаление системного мусора и кэша обновлений для повышения быстродействия диска.\n"
                "• **Целостность системы:** Сканирование и восстановление поврежденных файлов для обеспечения стабильности ОС.\n"
                "• **Калибровка сети:** Полный сброс сетевых параметров для минимизации задержек и стабилизации пинга.\n"
                "• **Игровой режим:** Приостановка фоновых служб для выделения максимума ресурсов CPU и RAM на игру.\n\n"
                "⚠️ **Важные предупреждения:**\n"
                "1. Интернет-соединение будет временно разорвано.\n"
                "2. Службы печати будут отключены до перезагрузки системы.\n"
                "3. **Запуск от имени администратора обязателен.**"
            ),
            "jp": (
                "🛡️ **[ Sel1Z SYSTEM STRATEGY v2.4 ]**\n\n"
                "**🚀 最適化の詳細:**\n"
                "• **高度なジャンク削除:** システムの残骸とWindows Updateキャッシュを徹底的にクリーンアップし、レスポンスを向上させます。\n"
                "• **システム整合性チェック:** OSの安定性を確保し、予期しないクラッシュを防ぐためにシステムファイルを修復します。\n"
                "• **ネットワーク調整:** ネットワークスタックを完全にリセットし、遅延（ラグ）を最小限に抑えてピンを安定させます。\n"
                "• **ゲームモード:** 不要なバックグラウンドサービスを一時的に停止し、CPUとRAMをゲームに優先的に割り当てます。\n\n"
                "⚠️ **重要な警告:**\n"
                "1. プロセス中にネットワーク接続が一時的に切断されます。\n"
                "2. 再起動するまでプリンター機能は無効になります。\n"
                "3. **完全に実行するには「管理者として実行」が必須です。**"
            )
        }

class LanguageSelect(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Thai", emoji="🇹🇭", value="th"),
            discord.SelectOption(label="English", emoji="🇺🇸", value="en"),
            discord.SelectOption(label="German", emoji="🇩🇪", value="de"),
            discord.SelectOption(label="Russian", emoji="🇷🇺", value="ru"),
            discord.SelectOption(label="Japanese", emoji="🇯🇵", value="jp"),
        ]
        # ต้องใส่ custom_id ที่ไม่ซ้ำใคร
        super().__init__(
            placeholder="Select Language / เลือกภาษา...", 
            options=options, 
            custom_id="persistent_lang_select"
        )
        
async def callback(self, interaction: discord.Interaction):
        # --- [จุดสำคัญ] สั่ง Defer เพื่อป้องกัน Interaction Failed ---
        await interaction.response.defer(ephemeral=True) 
        
        selected = self.values[0]
        desc = RESPONSES_DATA.get(selected, RESPONSES_DATA["en"])
        
        embed = discord.Embed(description=desc, color=0x990000)
        embed.set_footer(text="Developed by Sel1Z")
        
        # --- ใช้ followup แทน response เพราะเรา defer ไปแล้ว ---
        await interaction.followup.send(embed=embed, view=DownloadView(), ephemeral=True)

class LanguageView(ui.View):
    def __init__(self):
        super().__init__(timeout=None) # ห้ามมีวันหมดอายุ
        self.add_item(LanguageSelect())

# --- 3. Heartbeat Dashboard (ระบบไฟสถานะหน้าห้อง) ---
@tasks.loop(minutes=30) # ส่ง Log ทุกๆ 30 นาที
async def heartbeat():
    # เปลี่ยน ID แชนแนลที่ต้องการให้บอทส่ง Log (เอามาจาก Discord ของคุณ)
    LOG_CHANNEL_ID = 1482018260969979965  # <--- ใส่ ID ห้อง Log ของคุณตรงนี้
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        embed = discord.Embed(
            title="🛰️ SYSTEM HEARTBEAT",
            description=f"**Status:** `ONLINE` (Normal)\n**Last Sync:** `{now}`\n**Location:** `Railway Container`\n**Network:** `Connected`",
            color=0x00ff00 # สีเขียวแสดงว่าปกติ
        )
        embed.set_footer(text="Sel1Z Data Center Monitoring")
        await channel.send(embed=embed)

@bot.event
async def on_ready():
    # สำคัญที่สุด: ลงทะเบียน View ให้บอทรู้จักตลอดเวลาแม้เพิ่งจะ Restart
    bot.add_view(LanguageView())
    bot.add_view(DownloadView())
    
    # เริ่มระบบ Heartbeat
    if not heartbeat.is_running():
        heartbeat.start()
        
    print(f'>>> Sel1Z Bot is Online as {bot.user}')
    print(f'>>> Persistent Views Registered Successfully.')

@bot.command()
async def setup(ctx):
    embed = discord.Embed(title="[ Sel1Z ] SYSTEM STRATEGY", color=0x00ffff)
    embed.set_image(url="https://i.postimg.cc/4NjZjPSK/s-(5).png")
    embed.set_footer(text="Choose your language below to see the details.")
    await ctx.send(embed=embed, view=LanguageView())

# รันระบบ Web และ Bot
keep_alive()
bot.run(TOKEN)