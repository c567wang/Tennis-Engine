move_wo_des = []
unique_winners = []
for w in winners:
    if (w.shot_type,w.anchor) not in move_wo_des:
        unique_winners.append(w)
        move_wo_des.append((w.shot_type,w.anchor))
winners = unique_winners