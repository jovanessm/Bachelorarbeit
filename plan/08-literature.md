# Literature

## Verified ✅ (2026-11-09)
1. N. Bronson, A. Aghayev, A. Charapko, T. Zhu, "Metastable failures in distributed systems," HotOS '21, Ann Arbor, 2021, pp. 221–227, doi: 10.1145/3458336.3465286.
2. L. Huang et al., "Metastable failures in the wild," OSDI '22, Carlsbad, 2022, pp. 73–90.
   - Confirmed: ≥ 4 of 15 major AWS outages in the last decade; outages of 1.5 to 73.53 h (4–10 h most common); > 600 incident reports searched.
   - ❓ 21 vs. 22 failures: slides say 21 identified, abstract says in-depth study of 22 from 11 organizations. Check in the PDF which number refers to what.
   - Example code: github.com/lexiangh/Metastability
3. C. M. Aderaldo, T. M. Costa, D. M. Vasconcelos, N. C. Mendonça, J. Cámara, D. Garlan, "A declarative approach and benchmark tool for controlled evaluation of microservice resiliency patterns," Softw. Pract. Exper., vol. 55, no. 1, pp. 170–192, 2025, doi: 10.1002/spe.3368. (ResilienceBench)

## To verify ❓
- R. Isaacs et al., "Analyzing metastable failures," HotOS '25 (Crossref DOI 10.1145/3713082.3730380, first author Rebecca Isaacs, AWS).
- "Characterizing metastable faults and failures," preprint, Jun. 2026 (authors, venue).
- Arolla, "It's time to retry: ...", NSDI '27 submission (authors, title, status).
- Aderaldo & Mendonça, "How the retry pattern impacts application performance," SBES '23, doi: 10.1145/3613372.3613409 (candidate for related work).

## Still to do
Proper search in IEEE Xplore, ACM DL, Google Scholar: retry budgets, load shedding, deadline propagation, circuit breaker evaluation.
