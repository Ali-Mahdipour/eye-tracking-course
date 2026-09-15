# Day 1 concepts handout — Eye tracking essentials

**NBML workshop · Wed 25 Shahrivar 1405 / 2026-09-16 · In person**  
Instructors: Dr. Anahita Khorrami (cognitive framing) · Ali Golbazi Mahdipour (practical / hardware)

Keep this sheet on the desk during the lab. Short definitions only — details come in demos.

---

## 1. What the eye tracker measures

- **Gaze point:** where the eyes are pointing on the world / screen (2D or 3D).
- **Pupil size:** diameter of the pupil (lighting + cognition both matter).
- **Eye movements over time:** a sequence of stops and jumps.

Wearable systems (e.g. **Pupil Labs**) record the wearer’s viewpoint with a scene camera + eye cameras. Screen-based systems (e.g. **Tobii**) map gaze to a display and make AOIs easy.

---

## 2. Core event vocabulary

| Term | Everyday analogy | Typical signature |
|------|------------------|-------------------|
| **Fixation** | Eyes “parking” to take in information | Relatively still gaze for ~100–500+ ms |
| **Saccade** | Eyes “teleporting” to the next parking spot | Fast jump; little useful vision during the flight |
| **Smooth pursuit** | Eyes tracking a moving object | Continuous following (harder outdoors) |
| **Blink** | Brief blackout | Gaps / confidence drops in the signal |

**Nerd sticky note:** Fixations are the *what*; saccades are the *how you got there*. Analyses that only count fixations are reading the parking tickets and ignoring the roads.

---

## 3. Calibration (why it matters)

Calibration teaches the system how *your* eye images map to gaze directions.

- Bad calibration → beautiful heatmaps of the wrong place.
- Recalibrate after headset slip, glasses change, or large lighting change.
- Always do a **quick validation** (look at known targets) before the real trial.

---

## 4. Pupil Labs mental model (Day 1 tools)

1. **Capture** — live preview, calibration, recording.
2. **Recording folder** — video + gaze + pupil streams on disk.
3. **Player** — replay, plugins (fixation detector, etc.), export CSVs for analysis.

You will practice the loop: *fit → calibrate → record → replay → export*.

---

## 5. Quality checklist (before you trust a recording)

- [ ] Eyes visible in eye cameras; pupils not clipped
- [ ] Scene camera covers the task
- [ ] Calibration accepted / validation looks sane
- [ ] Confidence mostly high during the task
- [ ] Recording start/stop markers match the protocol
- [ ] Headset did not slip mid-trial

---

## 6. From lab today → analysis later

Exported tables (gaze, fixations, pupil) feed **Excel** (quick summaries) and **Python** (metrics, AOIs, pupillometry, plots). Bring a USB stick or cloud folder for your exports.

---

## 7. Mini glossary (EN / FA cues)

- Fixation / ثابت‌نگری  
- Saccade / ساکاد  
- Calibration / کالیبراسیون  
- Area of Interest (AOI) / ناحیه مورد علاقه  
- Dwell time / زمان اقامت  
- Scanpath / مسیر اسکن  

---

*Co-taught with NBML. Hardware support: NBML eye-tracking specialist on site.*
