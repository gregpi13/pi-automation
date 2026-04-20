# OpenGlass DIY Smart Glasses - Build Guide

**GitHub:** https://github.com/BasedHardware/openglass
**Community:** Based Hardware Discord
**Total Cost:** ~$20-25 CAD

---

## Parts List

### Required Components
1. **Seeed Studio XIAO ESP32 S3 Sense** — ~$15 CAD
   - Buy from: https://www.seeedstudio.com/
   - Or Amazon Canada search: "Seeed XIAO ESP32S3 Sense"

2. **EEMB LP502030 3.7v 250mAH battery** — ~$5 CAD
   - Amazon/eBay: "LP502030 lithium battery"
   - Specs: 3.7V, 250mAh, size 50x20x3mm

3. **3D Printed Glasses Mount** — Free (school printer!)
   - **STL Files:** https://www.thingiverse.com/thing:6643604
   - **File:** "Openglass (BasedHardware) case by chrisvolta"
   - **Includes:** Main case, frame front, temple arms
   - **Material:** PLA or PETG
   - **Print time:** ~2-4 hours
   - **Greg's plan:** Print at school

### Optional
- **Your own glasses frame** — Any regular glasses, cheap sunglasses, or safety glasses
  - **Clear non-prescription lenses** — Dollar store, hardware store safety glasses (~$2-5)
  - **Sunglass lenses** — Tinted, reduces camera glare, looks less conspicuous
  - **Existing frame** — Clip mount to glasses you already own
- **Soldering iron** — For battery connections
- **Jumper wires** — For connections

---

## Step-by-Step Build Instructions

### Step 1: Gather Parts
- [ ] Order XIAO ESP32S3 Sense
- [ ] Order battery
- [ ] 3D print mount case (or get printed)

### Step 2: Hardware Assembly
- [ ] Mount XIAO board into 3D printed case
- [ ] Connect battery (solder + to +, - to -)
- [ ] Attach mount to your glasses frame

### Step 3: Software Setup (Linux/Pi)
```bash
# Install Arduino IDE
sudo apt update
sudo apt install arduino

# Or use arduino-cli
wget https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh
sh install.sh
```

### Step 4: Configure Arduino
- [ ] Add ESP32 board package URL:
  - File > Preferences > Additional Boards Manager URLs:
  - `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
- [ ] Install ESP32 boards (Tools > Board > Boards Manager)
- [ ] Select board: XIAO_ESP32S3
- [ ] Set PSRAM: "OPI PSRAM" (Tools menu)

### Step 5: Flash Firmware
```bash
# Clone repository
git clone https://github.com/BasedHardware/openglass.git
cd openglass/firmware

# Open .ino file in Arduino IDE
# Select correct port (likely /dev/ttyUSB0)
# Click Upload
```

### Step 6: Install App
```bash
cd ~/openglass
npm install
# Or: yarn install
```

### Step 7: Configure API Keys
Edit `sources/keys.ts`:
- Add OpenAI key (for cloud AI)
- Add Groq key (alternative)
- OR configure Ollama (local): `http://localhost:11434/api/chat`

### Step 8: Setup Ollama (Optional - Local AI)
```bash
# If using Ollama instead of OpenAI
curl -fsSL https://ollama.com/install.sh | sh
ollama pull moondream:1.8b-v2-fp16
```

### Step 9: Start App
```bash
npm start
# Opens web interface at localhost
```

---

## What It Can Do

- **Record video** — First-person perspective
- **People recognition** — "Remember" faces with names
- **Object identification** — "What am I looking at?"
- **Text translation** — Translate signs/text in real-time
- **Life logging** — Record your day (optional)

---

## Pre-Built Kit Option

Don't want to DIY? Fill out interest form on GitHub:
- They sell limited pre-built kits
- Get notified when available
- Likely $50-100 vs $25 DIY

---

## Troubleshooting

- **Discord:** Based Hardware community
- **GitHub Issues:** https://github.com/BasedHardware/openglass/issues
- **Camera not working:** Check PSRAM setting
- **Won't connect:** Check battery polarity

---

## Connection to Your Pi

Since you already have Ollama running on your Pi:
1. Connect OpenGlass to same network as Pi
2. Point OpenGlass to Pi's IP: `http://[pi-ip]:11434/api/chat`
3. Run local AI without cloud costs!

---

*Added to memory: April 5, 2026*
