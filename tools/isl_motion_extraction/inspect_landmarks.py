import json

with open("tools/isl_motion_extraction/output/landmark_extraction_diagnostic.json", "r", encoding="utf-8") as f:
    data = json.load(f)

frames = data["frames"]
print(f"Total frames: {len(frames)}")

both_hands = []
neither_hands = []
left_only = []
right_only = []

for i, fr in enumerate(frames):
    lh = fr["leftHandDetected"]
    rh = fr["rightHandDetected"]
    if lh and rh:
        both_hands.append(i)
    elif not lh and not rh:
        neither_hands.append(i)
    elif lh:
        left_only.append(i)
    else:
        right_only.append(i)

print(f"Both hands detected ({len(both_hands)} frames): {both_hands}")
print(f"Neither hand detected ({len(neither_hands)} frames): {neither_hands}")
print(f"Left hand only ({len(left_only)} frames): {left_only}")
print(f"Right hand only ({len(right_only)} frames): {right_only}")

print("\n--- Hand Landmark Details at Peak (Frame 35) ---")
f35 = frames[35]
for hand_name, lms in [("Left Hand", f35["leftHandLandmarks"]), ("Right Hand", f35["rightHandLandmarks"])]:
    if lms:
        w = lms[0]
        i_mcp = lms[5]
        i_tip = lms[8]
        m_tip = lms[12]
        print(f"{hand_name} (21 joints):")
        print(f"  Wrist (0):    ({w['x']:.4f}, {w['y']:.4f}, {w['z']:.4f})")
        print(f"  IndexMCP (5): ({i_mcp['x']:.4f}, {i_mcp['y']:.4f}, {i_mcp['z']:.4f})")
        print(f"  IndexTip (8): ({i_tip['x']:.4f}, {i_tip['y']:.4f}, {i_tip['z']:.4f})")
        print(f"  MidTip (12):  ({m_tip['x']:.4f}, {m_tip['y']:.4f}, {m_tip['z']:.4f})")

# Let's inspect pose_world_landmarks if available
print("\n--- World Landmarks Availability ---")
print("poseWorldLandmarks in Frame 35:", len(f35.get("poseWorldLandmarks", [])))
if f35.get("poseWorldLandmarks"):
    pw_dict = {lm["id"]: lm for lm in f35["poseWorldLandmarks"]}
    # Joint IDs: 11=L_Shoulder, 12=R_Shoulder, 13=L_Elbow, 14=R_Elbow, 15=L_Wrist, 16=R_Wrist
    for jid, jname in [(11, "L_Shoulder"), (12, "R_Shoulder"), (13, "L_Elbow"), (14, "R_Elbow"), (15, "L_Wrist"), (16, "R_Wrist")]:
        j = pw_dict[jid]
        print(f"  {jname:11s} (id={jid:2d}): ({j['x']:+.4f}, {j['y']:+.4f}, {j['z']:+.4f}) meters")
