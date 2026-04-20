# EQAO Practice Tool - Companion Guide for Educators
## Complete Implementation Guide with Step-by-Step Prompts

---

## Table of Contents
1. [Quick Start: The Exact Prompt to Use](#quick-start)
2. [Technical Requirements & Setup](#technical-requirements)
3. [Step-by-Step Creation Process](#creation-process)
4. [Customization Guide](#customization)
5. [Distribution & Implementation](#distribution)
6. [Extension Ideas](#extensions)
7. [Troubleshooting](#troubleshooting)

---

## 1. Quick Start: The Exact Prompt to Use

### Primary Prompt Template

Copy and paste this into your AI tool (Copilot, ChatGPT, Claude, etc.):

```
Create an offline, self-contained HTML file for Grade [3/6] EQAO-style math practice. 

Requirements:
- Multiple practice tests (at least 5) covering: Number Sense, Measurement, 
  Geometry & Spatial Sense, Patterning & Algebra, Data Management & Probability
- Clean, student-friendly interface with large, readable fonts
- Works completely without internet after initial download
- Instant feedback: Show correct/incorrect immediately after each answer
- Progress tracker showing completion percentage
- No external dependencies - all CSS and JavaScript embedded in single HTML file
- Mobile-responsive design for tablets and Chromebooks
- Include simple instructions for students at the top

Include at least 10 questions per test, with a mix of:
- Multiple choice
- Short answer (numerical)
- Simple drag-and-drop or matching (if possible with HTML/CSS)

Make the design visually appealing with:
- Clear progress indicators
- Encouraging feedback messages
- Color coding (green for correct, red for incorrect with explanation)

Output: Provide the complete HTML code in a code block that I can save as a .html file.
```

### Prompt Variations by Grade

**For Grade 3:**
```
Create an offline, self-contained HTML file for Grade 3 EQAO-style math practice. 

Requirements:
- Focus on: Addition/subtraction to 1000, multiplication/division basics, 
  fractions, measurement (cm, m, g, kg, mL, L), time (5-minute intervals), 
  2D/3D shapes, simple patterns, basic data interpretation
- Large buttons and touch-friendly interface for young learners
- Visual representations where possible (shapes, number lines, pictures)
- Simple language at Grade 3 reading level
- Audio-friendly - works with screen readers if possible

[rest of requirements from primary prompt]
```

**For Grade 6:**
```
Create an offline, self-contained HTML file for Grade 6 EQAO-style math practice. 

Requirements:
- Focus on: All operations with whole numbers and decimals, fractions 
  (including improper/mixed), ratios and percent, measurement conversions, 
  area/perimeter/volume, angles and transformations, algebraic expressions, 
  data analysis and probability
- Scientific notation introduction
- More complex word problems
- Calculator-ready (optional button)
- Deeper explanations for wrong answers with solution steps

[rest of requirements from primary prompt]
```

---

## 2. Technical Requirements & Setup

### Compatible AI Tools

| Tool | Best For | Notes |
|------|----------|-------|
| **Microsoft Copilot** | Free, integrated | Good for basic versions |
| **ChatGPT (GPT-4)** | Complex interactions | May need Plus subscription |
| **Claude (Anthropic)** | Long outputs | Great for complete files |
| **Gemini** | Google's model | Free tier available |
| **Ollama (Local)** | Privacy-focused | Requires technical setup |

### System Requirements for Students

**Minimum:**
- Any modern web browser (Chrome, Firefox, Safari, Edge)
- Device with 4GB RAM
- 50MB free storage per practice file

**Recommended:**
- Tablet or laptop with keyboard
- Chromebook (very compatible)
- Updated browser (last 2 versions)

### File Specifications

- **Format:** Single .html file
- **Size:** 2-5 MB (text + embedded images as base64 if any)
- **No external links:** All CSS and JavaScript inline
- **Offline capable:** No CDN dependencies

---

## 3. Step-by-Step Creation Process

### Phase 1: Initial Generation (5 minutes)

1. **Open your AI tool**
   - Go to copilot.microsoft.com or your preferred tool
   - Ensure you're using the most capable model available

2. **Paste the prompt** from Section 1 above

3. **Review the output**
   - Check that you received complete HTML code
   - Verify it has `<html>`, `<head>`, `<body>` tags
   - Look for embedded CSS and JavaScript

4. **Save the file**
   - Copy the code from the AI response
   - Open Notepad (Windows) or TextEdit (Mac)
   - Paste the code
   - Save As: `EQAO_Grade3_Practice.html`
   - **Important:** Select "All Files" type, not .txt

### Phase 2: Testing (5 minutes)

1. **Open in browser**
   - Double-click the saved HTML file
   - It should open in your default browser

2. **Verify offline capability**
   - Disconnect WiFi/Ethernet
   - Refresh the page (F5)
   - Confirm it still works

3. **Test functionality**
   - Click through at least one complete test
   - Check instant feedback works
   - Verify progress tracker updates
   - Test on mobile device if available

### Phase 3: Refinement (10-15 minutes)

If the initial version isn't perfect, use these follow-up prompts:

**For more questions:**
```
Add 5 more questions to each test section, maintaining the same format 
and difficulty level. Ensure the HTML remains a single self-contained file.
```

**For design improvements:**
```
Improve the visual design: increase font size to at least 18px, add more 
white space between questions, use a calming color scheme (blues and greens),
and add a progress bar at the top.
```

**For accessibility:**
```
Add accessibility features: ARIA labels for screen readers, keyboard 
navigation support (Tab key), high contrast mode option, and ensure all 
images have alt text.
```

**For wrong answer explanations:**
```
For each question, add a detailed explanation that appears when the student 
answers incorrectly. Include: why the answer is wrong, the correct approach 
step-by-step, and a similar practice question.
```

---

## 4. Customization Guide

### A. Adding School Branding

```
Modify the CSS in the <style> section:

Replace colors:
- Find: background-color: #4CAF50;
- Replace with your school colors

Add school logo:
- Convert logo to base64: https://www.base64-image.de/
- Insert at top: <img src="data:image/png;base64,[your-code]" />
```

### B. Adjusting Difficulty

**Make it easier:**
- Request: "Reduce complexity: use smaller numbers (under 100), simplify 
  word problems, add visual hints, and allow multiple attempts without penalty"

**Make it harder:**
- Request: "Increase difficulty: add multi-step problems, include fractions 
  and decimals, reduce hint availability, and add time limits"

### C. French Version

```
Translate this entire HTML file to French, maintaining all functionality. 
Use Canadian French conventions and appropriate mathematical terminology 
for Ontario curriculum (e.g., "droite numérique" not "ligne numérique").
```

### D. Subject Variations

**For Literacy:**
```
Create an offline HTML reading comprehension practice tool for Grade 3. 
Include: short passages, multiple choice questions, vocabulary activities, 
and grammar practice. Follow Ontario Language curriculum strands.
```

**For Science:**
```
Create an offline Grade 6 science review tool covering: Life Systems 
(Biodiversity), Matter and Energy, Structures and Mechanisms, Earth 
and Space Systems. Include diagrams, matching activities, and mini-quizzes.
```

---

## 5. Distribution & Implementation

### Distribution Methods

**Option 1: USB Drives**
- Copy HTML file to USB drives
- Label clearly with grade level
- Include a "README - Start Here.txt" file

**Option 2: School Shared Drive**
- Upload to Google Drive/OneDrive/SharePoint
- Set permissions to "Anyone with link can view"
- Share link via email or LMS

**Option 3: Email to Parents**
- Attach HTML file directly to email
- Include instructions in email body
- Request confirmation of successful download

**Option 4: Class Website/LMS**
- Upload HTML file to your class webpage
- Students download once, use forever offline
- Update periodically with new versions

### Implementation Checklist

**Before distributing:**
- [ ] Tested on multiple devices (laptop, tablet, phone)
- [ ] Verified works offline
- [ ] Checked all links/questions work
- [ ] Proofread all text and explanations
- [ ] Saved backup copy

**First week with students:**
- [ ] Demonstrate opening the file in class
- [ ] Show students how to navigate
- [ ] Practice with one question together
- [ ] Explain instant feedback feature
- [ ] Set expectations for independent use

**Ongoing:**
- [ ] Track which students are using it
- [ ] Collect feedback for improvements
- [ ] Rotate different versions to prevent memorization
- [ ] Celebrate progress

### Student Instructions Template

Include this text file alongside the HTML:

```
🎯 EQAO Practice Tool - Student Instructions

1. SAVE the file:
   - Find the file named "EQAO_Practice.html"
   - Save it to your device (Downloads or Desktop)

2. OPEN the file:
   - Double-click the file
   - It will open in your web browser
   - NO INTERNET NEEDED after this!

3. PRACTICE:
   - Click "Start Test"
   - Answer each question
   - Click "Submit" to check your answer
   - Read the feedback - learn from mistakes!
   - Continue to next question

4. TRACK PROGRESS:
   - Watch the progress bar at the top
   - Try to complete at least one test per week

5. NEED HELP?
   - Ask your teacher if a question is unclear
   - Use pencil and paper for working out problems
   - Take your time - it's practice!

💪 Remember: Mistakes help you learn!
```

---

## 6. Extension Ideas

### Progress Tracking Spreadsheet

Create a companion Google Sheet where students log:
- Date of practice
- Test number completed
- Score achieved
- Topics needing more practice
- Goals for next session

### Differentiated Versions

Create three versions of each practice:
1. **Beginner:** Scaffolded hints, simpler numbers
2. **Standard:** Grade-level expectations
3. **Challenge:** Above-grade problems for advanced learners

### Gamification Add-ons

Request AI to add:
- Point systems and badges
- Unlockable achievements
- Progress certificates (printable)
- Class leaderboards (if collecting data)

### Parent Communication

Create a parent guide explaining:
- How the tool works
- Why offline practice matters
- How to support at home
- What questions to ask after practice

### Subject Integration

Combine multiple subjects into one file:
- Math problems based on science scenarios
- Literacy passages about math concepts
- Real-world problem solving across subjects

---

## 7. Troubleshooting

### Common Issues & Solutions

**Issue: File won't open**
- **Solution:** Ensure file extension is .html not .txt
- Try opening by right-click → Open With → Browser

**Issue: Images won't load**
- **Solution:** Check that images are embedded as base64
- Or replace with text descriptions

**Issue: Buttons don't work**
- **Solution:** Verify JavaScript is enabled in browser
- Check browser console for errors (F12)

**Issue: Progress not saving**
- **Solution:** Remind students: HTML files don't save progress automatically
- Suggest screenshotting final scores

**Issue: Wrong answers marked correct (or vice versa)**
- **Solution:** Check answer key in code
- Request AI to double-check all correct answers

**Issue: File too large**
- **Solution:** Remove base64 images, use text descriptions instead
- Split into multiple smaller files by topic

**Issue: Formatting looks wrong**
- **Solution:** Different browsers render differently
- Test in Chrome, Firefox, Safari, Edge
- Adjust CSS for cross-browser compatibility

### Getting Help

If stuck, try these resources:
1. **AI tool chat:** Paste the HTML code and describe the issue
2. **School IT department:** For technical troubleshooting
3. **Colleagues:** Share working files for inspiration
4. **Online communities:** r/education, Ontario teacher Facebook groups

---

## Quick Reference Card

**Print this and keep handy:**

```
📋 EQAO Tool Quick Reference

PROMPT: "Create offline HTML math practice for Grade [3/6]. 
Include 5+ tests, instant feedback, Ontario categories. 
Single file, no external links needed."

TIME: 20-30 minutes total
- Generate: 5 min
- Test: 5 min
- Refine: 10-20 min

DISTRIBUTE: USB, email, shared drive, or LMS

REMEMBER: Always test offline before sharing!

QUESTIONS? Re-prompt AI with specific fixes needed.
```

---

## Final Tips for Success

1. **Start simple** - First version doesn't need to be perfect
2. **Iterate quickly** - Use AI to make improvements in minutes
3. **Test early and often** - Verify offline functionality throughout
4. **Gather feedback** - Ask students what works and what doesn't
5. **Share with colleagues** - Pool resources and compare versions
6. **Keep backups** - Save different versions with dates
7. **Document your process** - Help other teachers learn from your experience

---

**Created:** April 2026  
**Purpose:** Support Ontario educators in creating offline, AI-assisted practice tools for student success  
**License:** Free to share and adapt for educational use

---

*This companion guide was created to accompany the EQAO Practice Tool presentation. Use it as a reference while creating your own tools, and adapt the prompts and processes to your specific classroom needs.*
