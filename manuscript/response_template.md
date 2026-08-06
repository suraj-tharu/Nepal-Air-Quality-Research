# Reviewer Response Document Template

**Manuscript ID:** [Insert Manuscript ID]
**Title:** [Insert Manuscript Title]

Dear Editor and Reviewers,

We would like to thank the Editor and the Reviewers for their thoughtful, constructive, and highly valuable comments. We have carefully considered all the feedback and have revised the manuscript accordingly. We believe these revisions have significantly improved the clarity, rigor, and overall quality of our paper.

Below, we provide a point-by-point response to all comments. The Reviewers' comments are reproduced in **bold**, our responses follow in plain text, and specific changes made in the revised manuscript are highlighted in blue text (or referenced by page/line number).

---

## Response to Reviewer #1

**General Comment from Reviewer 1:**
**[Insert Reviewer's general comment here]**

**Response:**
Thank you for your encouraging assessment of our work and the constructive feedback. We have addressed all your points below.

**Comment 1.1:**
**[Insert specific comment, e.g., "The authors should provide more details on why a 5km buffer was used for the Nepal boundary."]**

**Response:**
We appreciate the reviewer raising this point. The 5km buffer was applied to account for the spatial resolution of the Sentinel-5P TROPOMI data (approximately 5.5 km × 3.5 km) and to mitigate edge effects during the spatial aggregation near the national borders, particularly where transboundary pollution from the Indo-Gangetic Plain is prominent.

**Action Taken:**
We have clarified this methodological detail in Section 2.2 (Data Preprocessing) of the revised manuscript:
> *"To mitigate edge effects and account for the native spatial resolution of the Sentinel-5P TROPOMI sensor (approximately 5.5 × 3.5 km), a 5-km buffer was applied to the national boundary of Nepal prior to clipping the raster datasets (Smith et al., 2022)."* (Page X, Line Y)

---

**Comment 1.2:**
**[Insert specific comment, e.g., "Why wasn't ground validation data included for NO2?"]**

**Response:**
We completely agree with the reviewer that ground validation significantly strengthens satellite-based studies. However, a major limitation in Nepal is the severe sparsity of continuous, high-quality ground monitoring stations for trace gases like NO2 and SO2 (unlike PM2.5, which is monitored in the Kathmandu Valley). 

**Action Taken:**
While we could not perform a direct pixel-to-station validation due to data unavailability, we have heavily expanded our "Limitations" section to transparently address this issue. Furthermore, we have cross-referenced our S5P NO2 trends with published ground-sensor PM2.5 trends in Kathmandu to show temporal consistency. 
> *"A primary limitation of this study—and of regional atmospheric research in the Himalayas broadly—is the lack of a dense ground-based monitoring network for trace gases (NO₂, SO₂, HCHO). Consequently, direct pixel-to-station validation was not feasible. Future research should prioritize the deployment of reference-grade monitors across diverse physiographic zones to calibrate satellite retrievals."* (Section 4.4 Limitations, Page X)

---

## Response to Reviewer #2

**General Comment from Reviewer 2:**
**[Insert Reviewer's general comment here]**

**Response:**
We thank Reviewer #2 for their thorough review and insightful suggestions, particularly regarding the Wavelet Transform Coherence analysis, which has helped us refine our interpretation.

**Comment 2.1:**
**[Insert specific comment]**

**Response:**
[Provide response]

**Action Taken:**
[Detail exactly what was changed in the text]

---

Once again, we thank the Editor and Reviewers for their time and effort in evaluating our manuscript.

Sincerely,

[Your Name] on behalf of all co-authors.
