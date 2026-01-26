# ai_backeng/matching/merge_scores.py

def merge_scores(skill_scores, subject_scores, w_skills=0.7, w_subjects=0.6):
    final = {}

    for cid in set(skill_scores) | set(subject_scores):
        final[cid] = (
            w_skills * skill_scores.get(cid, 0) +
            w_subjects * subject_scores.get(cid, 0)
        )

    return final
