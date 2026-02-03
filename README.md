# Gesture-Triggered Autonomous Bubble System

An interactive visual system built using **MediaPipe**, **Python**, and **TouchDesigner** that creates autonomous digital bubbles through intentional human gestures.

---

## 🎯 Aim of the Project

To design an event-based interaction system where human gestures act as a **creation trigger** rather than continuous control.  
A bubble is created only at the moment a specific gesture combination occurs and then behaves independently.

---

## 🧠 Project Concept Overview

The system detects:

- Hand positions (left and right)
- Specific hand gestures (OK gesture)
- Facial input (mouth open)

When a defined gesture combination (e.g., **OK gesture + mouth open**) is detected, a bubble is spawned at the exact hand position **at that moment**.

After creation:

- The bubble no longer follows the body
- It moves autonomously
- User input is no longer required

---

## 🔬 System Architecture

The project is divided into logical layers:

### 1️⃣ Input Layer – Human Body to Data
- MediaPipe hand tracking
- Face landmark detection
- Continuous and noisy real-time data

### 2️⃣ Logic Layer – Gesture Interpretation
- Filters accidental motion
- Detects intentional gesture combinations
- Generates a short trigger pulse (0 → 1 → 0)

### 3️⃣ Spawn & Detachment Layer
- Samples hand X/Y only once
- Stores and holds the position
- Detaches visuals from live body data

### 4️⃣ Visual Behavior Layer
- Autonomous floating motion
- Noise-driven movement
- Smooth fade-in and fade-out

---

## 🫧 Visual Behavior

- Natural drifting motion
- Independent lifecycle
- Optional audio reactivity
- No continuous body dependency

---

## ⚠️ Design Philosophy

Traditional systems rely on continuous control.  
This project intentionally avoids that.

Instead, it explores **event-based interaction**, transforming the user from an operator into a performer.

---

## ✅ Expected Output

### Functional
- No visuals at rest
- Bubble appears only after valid gesture
- Bubble remains after gesture release
- Autonomous motion after creation

### Visual
- Minimal bubble design
- Smooth animation
- Clean detachment from live tracking

### Conceptual
- Gesture-based event triggering
- Expressive interaction
- Foundation for interactive installations

---

## 🎨 Applications

- Interactive art installations
- Live performance visuals
- Gesture-based creative tools
- Experimental HCI research
- Audio-visual environments

---

## 🛠️ Tools & Technologies

- **Python**
- **MediaPipe**
- **TouchDesigner 2025.32050**
- **OSC Communication**

---

## 🧩 Conclusion

This project demonstrates how intentional gestures can create expressive autonomous digital behavior.  
By separating creation from control, the system enables more natural and meaningful interaction.

---

## 📽️ Demo
(Add video or screenshots here)
