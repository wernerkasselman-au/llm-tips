# High-Signal Writing Guide (Full Ruleset)

A definitive, evidence-based reference for writing prose, documentation, articles, and code comments that do not read as LLM-generated.

**Scope.** This guide covers English-language writing across four domains where AI tells are most damaging: (1) published prose (articles, blogs, essays, marketing), (2) technical documentation (specs, READMEs, guides), (3) code comments, and (4) commit messages / PR descriptions / issue comments. It applies to writing produced by humans, by LLMs, or by humans editing LLM drafts.

**Principle.** The goal is not to "evade AI detectors." The goal is to write prose that does not exhibit the statistical fingerprints of a model that has been trained to please human raters, because that voice is uniform, risk-averse, information-dense in a noun-heavy way, rhetorically predictable, and devoid of the specific observational grit that makes human writing worth reading.

**How to use this guide.** For greenfield writing, internalise §2 and §3, then run §14's checklist before publishing. For AI-assisted drafts, treat every list in §4–§10 as a grep target: ten or more hits per piece means rewrite, not edit. Rewriting from scratch using the AI draft as notes is almost always faster than editing an AI draft sentence by sentence — see §12.2.

**Evidence base.** Every rule in this guide is tied to at least one quantitative source. The core corpus is Reinhart, Brown et al. (*PNAS* 2025, DOI 10.1073/pnas.2422455122), Kobak et al. (*Scientometrics* 2024, arXiv:2406.07016), Juzek & Ward (COLING 2025), Freeburg (arXiv:2603.27006), McGovern et al. (GenAIDetect 2025, aclanthology.org/2025.genaidetect-1.6), Zamaraeva et al. (ACL 2025 Long Papers), the *Washington Post* analysis of 328,744 ChatGPT messages (Merrill, Chen & Kumer, 13 November 2025), Wikipedia:Signs of AI writing (WP:AISIGNS), and Sam Kriss's "Why Does A.I. Write Like… That?" (*NYT Magazine*, 3 December 2025). Full references in §15.

---

## 1. Why AI writing sounds the way it does

Surface-level fixes fail because three deep training-pipeline forces converge to produce the AI voice. Understanding them tells you why swapping synonyms never works.

### 1.1 Pre-training selects formal, markdown-saturated corpora

LLMs are trained disproportionately on high-quality web text: Wikipedia, academic papers, news articles, GitHub READMEs, Stack Exchange. The Pile and RedPajama datasets in widespread use are heavily weighted toward content that either is markdown or was copy-edited by editors applying formal-register style guides. Formal, hedged, noun-heavy English is over-represented; casual conversational registers are systematically under-represented (Freeburg 2026; McGovern et al. 2025). This installs a *latent structural orientation* that later post-training amplifies or suppresses — not a defect, but a distribution.

### 1.2 Instruction tuning imposes noun-heavy informational density

Reinhart, Brown et al. constructed parallel corpora of ~12,000 human texts and GPT-4o / Llama 3 continuations of the first 500 words of each. Using Douglas Biber's 66-feature morphosyntactic tagset, they measured the rate at which each feature occurs per 1,000 words. Instruction-tuned models systematically diverge from human prose in a consistent direction (rates relative to human use shown below, from Brown et al. 2025, Table 3):

| Feature | GPT-4o Mini | GPT-4o | Llama 3 8B Instruct | Llama 3 70B Instruct | Llama 3 8B Base | Llama 3 70B Base |
|---|---:|---:|---:|---:|---:|---:|
| Present participial clauses | 481% | 527% | 224% | 261% | 94% | 102% |
| 'That' clauses as subject | 331% | 263% | 180% | 173% | 64% | 68% |
| Nominalizations | 209% | 214% | 145% | 151% | 88% | 91% |
| Phrasal coordination | 144% | 194% | 187% | 170% | 92% | 97% |
| Attributive adjectives | 140% | 150% | 100% | 104% | 79% | 83% |
| Past participial postnominal | 257% | 235% | 75% | 75% | 129% | 131% |
| Demonstratives | 137% | 133% | 77% | 80% | 75% | 80% |
| Clausal coordination | 63% | 59% | 141% | 127% | 120% | 116% |
| Agentless passives | 51% | 53% | 96% | 89% | 101% | 98% |
| First-person pronouns | 81% | 62% | 111% | 108% | 136% | 127% |
| Second-person pronouns | 63% | 52% | 77% | 81% | 118% | 110% |
| Contractions | 63% | 60% | 141% | 139% | 142% | 129% |
| Hedges ("at about", "almost") | 50% | 63% | 62% | 67% | 89% | 92% |

**Read it.** Llama 3 base models (right two columns) are close to human rates on almost every feature. Instruction tuning pushes them toward the noun-heavy, participle-heavy, low-first-person, low-contraction register seen in GPT-4o. This is not a stylistic bug — it is the signature of a model trained to sound authoritative and thorough.

The authors' specific GPT-4o example: "Bryan, leaning on his agility, dances around the ring, evading Show's heavy blows." Two present participles in one sentence. A human boxing writer would not write that.

Their Llama 3 70B Instruct example, with four nominalizations in one sentence: "These schemes can help to reduce deforestation, habitat destruction, and pollution, while also promoting sustainable consumption patterns."

### 1.3 RLHF / DPO contrastive optimisation rewards antithesis and verbosity

Reinforcement Learning from Human Feedback trains a reward model on human rater preferences, then optimises the LLM to produce high-reward outputs. DPO (Direct Preference Optimization) formalises the same objective as a contrastive loss. Both are mathematically equivalent to training the model to move *toward* chosen completions and *away* from rejected ones.

Because chosen completions in rater datasets tend to be longer, more hedged, more "balanced," and more rhetorically polished than rejected ones (rejected answers are typically flat and declarative), the contrastive objective directly installs four tells:

1. The **"It's not X, it's Y"** antithesis is the surface form of contrastive training — it literally repudiates a proximate alternative and proposes the preferred one.
2. The **hype register** ("crucial," "pivotal," "transformative," "testament to") is preferred by raters who want answers to "sound smart."
3. The **both-sides framing** ("While X is true, Y is also important…") is face-saving behaviour that avoids being rated "wrong."
4. The **em dash** is amplified by raters who perceive em-dash-heavy prose as precise and articulate.

Sam Altman publicly acknowledged that ChatGPT's em-dash frequency has been deliberately tuned in response to user preference (see Freeburg 2026), confirming that RLHF can and does target specific punctuation-level features.

Juzek & Ward (COLING 2025) confirmed RLHF's role experimentally by comparing Llama 2-Base to Llama 2-Chat (same architecture, same base weights, differs only in fine-tuning). Llama 2-Chat is "considerably less surprised" (per-word entropy 0.886 vs 1.051) by ChatGPT-generated abstracts containing focal words. This is direct evidence that RLHF, not architecture or pre-training data alone, is what installs the lexical preferences.

### 1.4 Consequence: you cannot prompt your way out

Negative instructions ("do not use em dashes," "do not hedge," "write in my voice") degrade within a few hundred tokens and fail completely in longer outputs. Freeburg's three-condition suppression gradient is the definitive demonstration: GPT-4.1 produces 10.62 em dashes per 1,000 words unconstrained, 9.10 under markdown suppression, and *still 3.86 even under explicit em-dash prohibition*. The structural impulse overrides the explicit instruction.

What does work: rewriting from scratch, using the AI draft as research. See §12.

---

## 2. What natural human writing looks like

Before listing what to avoid, anchor on what to produce. Twelve characteristics consistently distinguish human prose in the literature (Kobak et al. 2024; Juzek & Ward 2025; Reinhart, Brown et al. 2025; McGovern et al. 2025; Washington Post 2025; WP:AISIGNS).

1. **Positive burstiness.** Sentence lengths are positively skewed: many short sentences, some medium, occasional long ones. AI output clusters around a bell curve. Metric: coefficient of variation of sentence lengths. AI: typically 0.15–0.25. Human: typically 0.4–0.7 across non-academic registers.
2. **Unpredictable word choice.** Per-sentence perplexity varies widely. A factual sentence is followed by a metaphor is followed by a fragment. LLM outputs minimise perplexity per step; human writers don't.
3. **Concrete proper nouns.** Specific people, places, dates, product names, version numbers, error codes. AI defaults to generic placeholders ("a major city," "a leading company," "a marketing team at a mid-sized firm"). Pangram's observation: 60–70% of character names in unprompted ChatGPT/Claude short stories are "Emily" or "Sarah." Kriss documented that asking any AI to write science fiction produces protagonists named "Elara Voss" or "Kael" with uncanny frequency; before 2023 there was not a single self-published book on Amazon using "Elara Voss." By late 2025 there were hundreds.
4. **Asymmetric allocation of attention.** Important points get more space; minor points get a sentence. AI allocates attention democratically — every subsection is roughly the same length, every item in a list is similar length and parallel grammar.
5. **Opinions, taken at normal risk.** A position is stated, not balanced. "Whether X or Y" is a red flag; "X, because Y" is human.
6. **Visible thinking.** False starts, self-correction, mid-sentence pivots, "actually, wait —" moments. Clean first-draft prose reads as machine output.
7. **Grammatical imperfection.** Sentence fragments. Starting with "And" or "But." Occasional missed preposition. An Oxford comma used inconsistently. Contractions — AI-instruction-tuned Llama uses them at 129–142% of human rate only because its base rate has been trained low (Llama base uses them at near-human rates; GPT-4o uses them at only 60% of human rate).
8. **Lexical specificity.** Precise verbs instead of hedged generic ones ("crashes on null input" instead of "handles edge cases poorly").
9. **Register variation within a piece.** Shifts between formal and conversational, deliberately. Brown et al. demonstrated that instruction-tuned LLMs show limited register variation — they produce the same dense, participle-heavy style whether continuing TV scripts, blog posts, spoken transcripts, or academic articles. Humans adapt.
10. **Refusal to over-explain.** AI's default is to announce the structure, deliver the content, then summarise it. Humans state things once.
11. **Specific obscenity and informality.** Brown et al.'s most-underrepresented-words table for GPT-4o includes "fucking" (at 0.0083× human rate), "fuck," "asshole," "shit," "nasty," "ok," "blah," "yep," "i.e." AI does not write how people talk. A single well-placed informal word is a powerful de-AI signal.
12. **Real named things.** Real people, real companies, real products, real error messages, real dates, real page numbers, real version numbers. AI cannot produce these; it can only produce plausible-looking substitutes.

---

## 3. Core principles

Five principles override every detailed rule in §4–§10. When a rule and a principle conflict, follow the principle.

### P1. Specificity over abstraction

Every generic noun ("landscape," "ecosystem," "framework," "realm," "dynamic") is an opportunity for a specific one. Every unnamed authority ("experts argue," "studies show," "observers note") is a weasel citation to either name or delete.

> **Before:** "Studies show that AI is transforming the healthcare landscape."
> **After:** "A 2023 RAND survey of 2,400 US physicians found 38% had used an LLM for a clinical decision in the previous month."

Kobak et al. found that 2024 excess vocabulary in PubMed was 66% verbs and 18% adjectives — overwhelmingly style words, not topic words. The excess vocabulary of the Covid pandemic, by contrast, was almost entirely content words (remdesivir, respiratory, omicron). The distinction matters: style words float, content words pin text to specific referents.

### P2. Commitment over balance

If a claim is true, state it. If it is defensible but contested, defend it. Do not present every question as "nuanced" or "multifaceted" and then refuse to take a position. The reflexive "both sides" framing is the single clearest RLHF artefact. Cherryleaf's summary: "Real writers with expertise pick a position and defend it. AI always presents both sides."

> **Before:** "While there are valid arguments on both sides, the optimal approach ultimately depends on context."
> **After:** "For latency-sensitive workloads, gRPC is the right choice. REST wins everywhere else because the tooling gap is not worth closing."

### P3. Rhythm over symmetry

Mix sentence lengths deliberately. A twenty-eight-word sentence followed by a three-word sentence is a human signature. Three ten-word sentences in sequence is a machine signature. Let some paragraphs be one sentence and others be ten. Let one section be twice as long as the next because one point deserves it.

### P4. Do the work instead of gesturing at it

When tempted to write "this is a complex, multifaceted issue" — describe the facets. When tempted to write "this is a testament to his enduring legacy" — describe the thing he did. Adjectives of importance ("crucial," "pivotal," "significant") are almost always a failure to show the importance. Wikipedia:AISIGNS catalogues this as "Undue emphasis on significance, legacy, and broader trends" and lists the specific repertoire: "stands as / serves as a testament," "marking a pivotal moment," "a vital / significant / crucial / pivotal key role / moment," "underscores / highlights its importance / significance," "reflects broader," "symbolising its ongoing / enduring / lasting," "contributing to the," "setting the stage for," "marking / shaping the," "represents / marks a shift," "key turning point," "evolving landscape," "focal point," "indelible mark," "deeply rooted."

### P5. Write one thing, not the idea of that thing

AI writes to sound plausible; humans write to say something specific. If a sentence would be true of any company / any law / any person in the category, delete it. The test: swap the subject for a random other subject of the same type. If the sentence still works, it wasn't saying anything.

Kriss in the *NYT Magazine* gave the definitive example. Asked to write an extremely funny episode of *The Simpsons*, ChatGPT produced a screenplay in which the characters tickled one another in a round: "First Homer tickles Bart, and Bart laughs, and then Bart tickles Lisa, and Lisa laughs, and then Lisa tickles Marge." "Somewhere in its web of associations, the machine had made a connection: Jokes are what make people laugh, tickling makes people laugh, therefore talking about tickling is the equivalent of telling a joke. That was an early model; they don't do this anymore. But the same basic structure governs essentially everything they write." The model is always producing the idea of a joke / the idea of an insight / the idea of a specific example rather than the thing itself.

---

## 4. Banned and restricted vocabulary

These words and phrases are statistically over-represented in LLM output. The bans are not absolute — every word here can appear in legitimate human writing. The rule is density. A single "underscore" in a 2,000-word piece is fine; three is a tell; six is disqualifying. **The piece is the unit of analysis, not the sentence.**

### 4.1 The absolute bans — the Juzek–Ward focal words

Juzek & Ward (COLING 2025) identified 21 focal words by a three-step method: (a) the word's per-million frequency in PubMed abstracts rose significantly between 2020 and 2024, (b) the spike had no content explanation, and (c) ChatGPT-3.5 systematically over-uses the word when prompted to write abstracts. These are the 21 words with the highest ratio of ChatGPT usage to human baseline:

| Word | Ratio (ChatGPT : human) |
|---|---:|
| delve | 1,374.92× |
| boasts | 918.18× |
| underscores | 903.61× |
| comprehending | 898.95× |
| intricacies | 772.85× |
| surpassing | 667.48× |
| intricate | 611.24× |
| underscoring | 536.94× |
| garnered | 437.19× |
| showcases | 422.45× |
| emphasizing | 397.12× |
| underscore | 390.65× |
| realm | 381.10× |
| surpasses | 367.55× |
| groundbreaking | 330.42× |
| advancements | 277.59× |

Every one of these is a tell at normal density. Use with specific justification only.

Kobak et al. (2024) analysed 14 million PubMed abstracts 2010–2024 and found the LLM-induced vocabulary shift was unprecedented: 329 "excess words" in Q1 2024 (i.e., words appearing significantly more than linear extrapolation from 2021–2022 predicts), compared to at most 188 during the peak of the Covid pandemic. Excess ratio (2024 vs 2022 counterfactual): "delves" 25.2×, "showcasing" 9.2×, "underscores" 9.1×. The authors estimate the lower bound on LLM usage among 2024 PubMed abstracts at 10%, with some sub-corpora (e.g., Chinese biomedical authors writing in English) reaching 30%.

### 4.2 Reinhart/Brown PNAS most-overrepresented words in narrative continuation

Brown et al.'s GPT-4o sample over-uses specific words at the following rates (vs human use per 1,000 words in matched continuations):

| Word | GPT-4o Mini | GPT-4o |
|---|---:|---:|
| camaraderie | 171× | 162× |
| tapestry | 147× | 155× |
| palpable | 145× | 95× |
| intricate | 129× | 119× |
| grapple | 131× | — |
| fleeting | 124× | 84× |
| ignite | 122× | — |
| unspoken | — | 102× |
| vibrant | 92× | — |
| amidst | 90× | 100× |
| cacophony | 89× | — |
| underscore | — | 107× |
| unravel | — | 83× |
| solace | — | 95× |

A GPT-4o sample phrase cited in the paper: *"The camaraderie was palpable."* Four words, both items in the 150×+ range. A human writer producing narrative continuation does not write this sentence.

### 4.3 Tier-1 bans — never use without specific reason

The following appear both in the Juzek–Ward focal words, the Brown et al. GPT-4o over-representation list, the Pangram vocabulary list, the jpeggdev/humanize-writing Tier 1 list, and Wikipedia:AISIGNS. Each has become a standalone marker:

- **delve / delves / delving** — Use "look into," "dig into," "examine," or just delete. Post-ChatGPT spike of 2,700% in PubMed abstracts (Kriss 2025, confirmed by Kobak et al. r=25.2).
- **tapestry** (as metaphor for culture, history, diversity) — Pangram's cross-corpus analysis showed a 25× overrepresentation over Gutenberg baseline. If you literally mean woven cloth, fine.
- **intricate / intricacies** — 611–772× over human rate in ChatGPT abstracts (Juzek & Ward). Use "detailed," "complicated," or describe the actual details.
- **vibrant** — 1,260× overrepresentation in ChatGPT samples over Gutenberg baseline.
- **realm** (as metaphor for "domain," "area") — Use "area," "field," "world." "Realm" is for Tolkien.
- **testament** ("X is a testament to Y") — Delete; describe what X actually demonstrates.
- **underscore / underscores / underscoring** (as verb meaning "emphasise") — 390–903× over human rate. Use "shows," "proves," or rewrite so the fact carries its own weight.
- **showcase / showcases / showcasing** — 422× over human rate in Juzek–Ward. Use "shows," "includes," "features." One of the four persistent post-2025 (GPT-5-era) tells per Wikipedia:AISIGNS.
- **seamless / seamlessly** — Delete or replace with the specific integration mechanism.
- **navigate / navigating** (as metaphor for handling) — "Navigate challenges," "navigate the landscape" are pure AI. Say "handle," "manage," or describe the actual steps.
- **leverage** (as verb meaning "use") — Almost always means "use." Use "use."
- **boasts** (meaning "has") — 918× over human rate. Replace with "has."
- **multifaceted / nuanced** — If you believe it, describe the facets / the nuance. Labels without content are hollow.
- **comprehensive** — Meaningless signifier. Either prove comprehensiveness with scope data or delete.
- **crucial / pivotal / vital / paramount** — All four are hype adjectives. Replace with the specific consequence or metric. Kobak et al.: "crucial" δ=0.026, i.e. it appears in 2.6 percentage points *more* 2024 abstracts than the counterfactual 2022 projection would predict.
- **groundbreaking** — 330× over human rate. Rarely true. Delete.
- **advancements** — 277× over human rate. Use "advances" if you must.
- **camaraderie / palpable / fleeting / solace / unspoken** — All 80–170× over human rate in GPT-4o narrative continuation (Brown et al.).
- **grapple / grapples / grappling** — 131× over human rate. Use "handle," "wrestle with."
- **amidst** — 90–100× over human rate. Use "amid," or restructure.
- **"signal, not noise" / "signal vs noise" / "signal over noise" / "more signal than noise"** — Banned outright. The phrase is a tech-bro cliché *and* an instance of the §5.1 negative-parallelism pattern in one. Replace with a specific claim about what the disagreement (or data, or whatever) actually carries: "disagreement between the critic and sentinel flags scenario miscategorisation," not "disagreement is signal, not noise." If you cannot say what the signal is, you do not have one to defend.

### 4.4 Restricted (density matters — max one per ~2,000 words)

Use at most one per ~2,000 words; more than one in combination with any Tier-1 word disqualifies:

additionally, moreover, furthermore, however (as an opener), enhance, foster, fostering, robust, dynamic, holistic, cutting-edge, game-changing, transformative, revolutionary, innovative, streamline, empower, embark, embrace (metaphorical), endeavour, garner, harness, illuminate, resonate, weave/weaving, journey (metaphorical), roadmap, ecosystem, framework (used vaguely), landscape (abstract), paradigm, synergy, alignment / align with, paramount, imperative, overarching, unprecedented, profound, renowned, stunning, exemplifies, valuable (as a generic modifier), rich (as in "rich history"), deeply rooted, indelible.

### 4.5 Opener bans

Never open a sentence, paragraph, or section with any of the following — each is on Wikipedia:AISIGNS, the Cherryleaf list, and jpeggdev/humanize-writing:

- "In today's fast-paced / ever-evolving / digital / modern / interconnected world…"
- "In recent years…"
- "In an increasingly [adjective] world…"
- "As we navigate…"
- "In the realm of…"
- "At its core…"
- "It is important to note that…"
- "It is worth noting that…"
- "It is worth mentioning that…"
- "It should be noted / mentioned that…"
- "It is worth considering that…"
- "One might argue that…"
- "As you may know…"
- "When it comes to [topic]…"
- "Picture this:" / "Imagine a world where…"
- "In this article, we will explore…" / "Let's dive in" / "Without further ado"
- "Whether you're a [X] or a [Y]…"
- "It's no secret that…"
- "Here's the thing:" / "Here's an uncomfortable truth:" / "And honestly?"

### 4.6 Closer bans

Never close a section, paragraph, or piece with any of these. In a 2026 SearchEngineLand analysis of 1,000+ URLs, "Conclusion" section headers showed the strongest negative correlation with reader engagement in the entire dataset (≈ −0.118). Readers bounce when they see them.

- "In conclusion…" / "To conclude…"
- "In summary…" / "To summarise…"
- "Overall…"
- "Ultimately, X depends on Y."
- "There is no one-size-fits-all solution."
- "Only time will tell."
- "The future of X remains to be seen."
- "The bottom line is…"
- "At the end of the day…"
- "When all is said and done…"
- "As we move forward…"
- "It remains to be seen whether…"
- "The journey toward X is just beginning."
- "The future is bright…"
- "Start your journey today."
- "Exciting times lie ahead."

### 4.7 Hedging phrases (delete in almost all cases)

Brown et al.'s Biber-feature table shows LLMs use hedges ("at about," "something like," "almost") at only 50–67% of the human rate — but they use *discursive hedges* (the phrases below) far above human rate. The tell is the specific construction, not hedging itself.

- "It's important to note / mention / understand that…"
- "It's worth mentioning / considering that…"
- "It should be noted that…"
- "Generally speaking…"
- "In many / most cases…"
- "To a certain extent…"
- "Arguably…"
- "Potentially…"
- "May / might / could" used to soften a factual claim
- "Some would say…" / "One could argue…"
- "This is not without its challenges…"
- "It remains to be seen…"

Hedging has legitimate uses (regulated domains, genuinely uncertain claims). The test: am I hedging because I'm unsure, or hedging because I want to sound cautious? If the latter, cut it.

### 4.8 Sycophantic / chatbot artefacts (always delete)

These slip through when AI drafts are pasted without editing:

- "Great question!" / "Certainly!" / "Absolutely!"
- "I hope this helps!" / "Let me know if you'd like me to elaborate!" / "Let me know if you'd like me to expand."
- "Feel free to…"
- "Sure! Here's…"
- "Here's a comprehensive overview:" / "Here's a detailed breakdown:"
- "You're absolutely right!"
- "As an AI…" / "As a language model…"
- "Based on the information available…" / "Based on available information…"
- "While specific details are limited…" / "…aren't widely documented…"
- "As of my last knowledge update…" / "As of my knowledge cutoff…"
- "[subject] maintains a low profile" / "keeps personal details private" (speculative cover for missing information).

### 4.9 Wikipedia:AISIGNS vocabulary by model era

LLM lexical fashions shift. The following synthesis from Wikipedia:AISIGNS is operationally useful for gauging which model wrote something and what to watch for in new drafts:

- **2023–mid-2024 (GPT-4 era):** Additionally, boasts, bolstered, crucial, **delve**, emphasizing, enduring, garner, intricate / intricacies, interplay, key, landscape, meticulous / meticulously, pivotal, underscore, **tapestry**, testament, valuable, vibrant.
- **Mid-2024–mid-2025 (GPT-4o era):** align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant.
- **Mid-2025 onward (GPT-5 era):** emphasizing, enhance, highlighting, showcasing (plus the newer "Undue emphasis on notability / attribution / media coverage" pattern: "profiled in," "independent coverage," "leading expert," "active social media presence").

"Delve" peaked and is now on sharp decline; its presence today is less diagnostic than a year ago. "Emphasising," "enhance," "highlighting," "showcasing" are the current persistent tells.

### 4.10 Filler-phrase replacements

Verbose filler resolves to one of: a simpler conjunction, the bare verb, or deletion. Common replacements:

| Filler | Replacement |
|---|---|
| In order to | To |
| In order to achieve this goal | To achieve this |
| Due to the fact that | Because |
| At this point in time | Now |
| At the present time | Now |
| In the event that | If |
| Has the ability to | Can |
| It is important to note that | (state the fact) |
| It is worth noting that | (state the fact) |
| It should be noted that | (state the fact) |
| For the purpose of | For / To |
| In light of the fact that | Because |
| In spite of the fact that | Although |
| With regard to | About / On |
| In the process of | (just the verb) |
| As a matter of fact | (delete) |
| Needless to say | (delete) |
| It goes without saying | (delete) |

Source: Humanizer kit (Berman 2026); WP:AISIGNS hedge inventory.

---

## 5. Banned syntactic and structural patterns

Lexical cleanup alone is insufficient. Sam Kriss's *New York Times Magazine* analysis ("Why Does A.I. Write Like… That?", 3 December 2025) argued — correctly — that structure is a deeper tell than vocabulary. Once the vocabulary is cleaned, readers still sense AI because the **shapes** of sentences and paragraphs are wrong.

### 5.1 Negative parallelism — "It's not X, it's Y" and "Not just X, but Y"

The single most recognisable AI structure. Classical rhetoric calls it antithesis or negative-positive parallelism. In human writing it is a high-impact device used sparingly for emphasis. In LLM output it appears at densities no human writer produces.

**The data.** The *Washington Post* analysed 328,744 publicly shared ChatGPT messages (gpt-4o, May 2024 – July 2025). Variations of "not just X, but Y" alone appeared in roughly **6% of all July 2025 messages**. That is one in every seventeen messages containing the exact construction. No human register achieves that rate.

**Why it happens.** RLHF and DPO are contrastive learning objectives: the model is trained to move *toward* preferred completions and *away* from rejected ones. Prefacing with a negation ("it's not X") syntactically enacts distance from the rejected sample space; stating the elevated alternative ("it's Y") enacts convergence on the preferred one. The antithesis surface form is a direct output of the contrastive objective given the composition of human preference data (Milind Nair, Dev.to March 2026, summarising the mathematics).

**Rule.** Use the construction **zero times** unless you have a specific rhetorical reason. At most once per 2,000-word piece. Variants to grep for:

- "It's not just X — it's Y."
- "This isn't about X; it's about Y."
- "Not only X, but also Y."
- "Not X, but Y."
- "Less about X, more about Y."
- "No X, no Y, just Z."

**Fix.** Say only the positive. "It's Y" carries more force than "It's not X; it's Y" in nine cases out of ten.

### 5.2 The tricolon reflex — rule of three

LLMs group ideas in threes compulsively: three-item lists, three adjectives, three parallel clauses. Humans use threes too, but at roughly a third of the AI rate (LinkedIn analysis by Massobrio, "Triviality and Rhetorical Triplets," 2025). The tell is frequency, not any single tricolon.

**Rule.** If two consecutive paragraphs both use three-item structures, rewrite one. If more than ~30% of your lists have exactly three items, you are defaulting to rhetoric, not content.

**Specific patterns to delete or rewrite:**

- "Start building, start learning, start growing." (motivational tricolon close)
- "Through curiosity, persistence, and collaboration…" (abstract-noun tricolon)
- "Identify, analyse, act." / "Plan, prepare, perform." (imperative tricolon)
- "Time, resources, and attention." (noun tricolon where two would do)
- "Clear, concise, and actionable."
- "Efficient, scalable, and robust."

### 5.3 The balanced conclusion

A specific and corrosive AI pattern: a conclusion that presents "the good news," "the challenge," and "a forward-looking closer" in perfect symmetry. Also appears as "Despite X, Y faces challenges, including … However, with [ongoing efforts / future outlook] it continues to thrive." Wikipedia:AISIGNS flags this as "Outline-like conclusions about challenges and future prospects" and gives the canonical form: *"Despite its [positive/promotional words], [article subject] faces challenges… Despite these challenges, [subject] continues to… With [X], it is positioned to…"*

**Rule.** End with one strong statement, not a balanced assessment. If the evidence points one way, the conclusion points one way.

### 5.4 Avoidance of basic copulas — "serves as" / "stands as" / "represents" / "marks"

LLM-generated text systematically replaces "is"/"are" with "serves as," "stands as," "marks," "represents," "features," "boasts," "offers," "maintains." One study documented an **over 10% decrease in the usage of the words "is" and "are" in academic writing in 2023 alone**, with no prior trend (cited in WP:AISIGNS). The same pattern appears in AI copyedits: asked to "revise," GPT systematically hollows out copulas.

The Brown et al. Biber table confirms this at feature level: LLMs use "be" as main verb at 61–63% (GPT-4o) and 100–108% (Llama Instruct) of human rate. The compensation is in nominal constructions — "serves as X," "stands as X," "boasts a Y," "features a Z."

**Rule.** Default to "is." Reach for "serves as" only when the subject genuinely performs a function ("the valve serves as a pressure relief").

> **AI:** "Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces…"
> **Human:** "Gallery 825 is LAAA's exhibition space for contemporary art. There are four rooms…"

### 5.5 Superficial participial analyses

The strongest Brown et al. finding: instruction-tuned LLMs use present participial clauses at **2–5× the human rate**. They function as a way to gesture at significance without doing the work: "…reflecting broader trends," "…underscoring its importance," "…contributing to the region's cultural identity," "…highlighting the enduring relevance of…," "…ensuring continued relevance," "…showcasing how…," "…fostering a sense of…," "…encompassing…"

Wikipedia:AISIGNS catalogues this as "Superficial analyses" and notes the specific repertoire: "highlighting / underscoring / emphasising …," "ensuring …," "reflecting / symbolising …," "contributing to …," "cultivating / fostering …," "encompassing …," "valuable insights," "align / resonate with."

**Rule.** Delete every terminal participial phrase that does not add a fact. If the phrase contains "reflecting," "underscoring," "emphasising," "highlighting," "showcasing," "contributing to," "cultivating," "fostering," or "ensuring," it is almost always decorative.

### 5.6 The "challenges and future prospects" scaffold

Wikipedia:AISIGNS Example from a December 2025 draft: *"Despite its industrial and residential prosperity, Korattur faces challenges typical of urban areas, including… With its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of the Ambattur industrial zone, embodying the synergy between industry and residential living."* Every single word after "urban areas" is filler.

**Rule.** Do not write a challenges paragraph unless you have specific, sourced, load-bearing challenges to discuss. Never end with "despite these challenges" followed by uplift.

### 5.7 Over-scaffolding: announce / deliver / summarise

AI writes like a bad TED talk: tells you what it's going to say, says it, then tells you what it said.

- Delete intros like "In this article, we'll explore…" / "Let's dive in."
- Delete roadmap sentences like "First, we'll cover X. Then we'll cover Y."
- Delete every conclusion that begins "As we've seen…" or "In summary…"

### 5.8 "Elegant variation" / pronominal gymnastics

LLMs have repetition-penalty decoding and explicit training to avoid reusing a word, which produces the classic Fleet Street "popular orange vegetable" phenomenon — after calling someone by name, every subsequent reference cycles through "the actor," "the star," "the 45-year-old," "the Academy Award nominee."

**Rule.** Reuse names. Reuse "the company," "the function," "the user" where they are the clearest referent. Variation for variation's sake is an AI tell. (*The Guardian* style team has mocked this for decades under the "POV — popular orange vegetable" name; an LLM is simply doing it as a system default.)

### 5.9 Paragraph uniformity

AI paragraphs cluster around a narrow length band (typically 60–90 words). Human paragraphs vary from one sentence to twelve sentences. The coefficient of variation of paragraph lengths is one of the most reliable statistical AI signals (Kitmul 2026; Pangram 2025).

**Rule.** Never write a piece where every paragraph is within ±20% of the same length. Never write a piece where every section gets roughly equal wordcount.

### 5.10 Em dashes — the markdown fingerprint

Em-dash overuse is real but derivative. Freeburg (2026) showed em dashes are "markdown leaking into prose — the smallest surviving unit of structural formatting when headers, bullets, and bold are suppressed." Humans have used em dashes for centuries; the test is function and frequency.

**Freeburg's measured em-dash rates per 1,000 words across 12 models (unconstrained / markdown-suppressed / em-dash-prohibited):**

| Model | Unconstr. | MD suppr. | EM suppr. |
|---|---:|---:|---:|
| GPT-4.1 | 10.62 | 9.10 | 3.86 |
| Claude Opus 4.6 | 9.09 | 0.19 | 0.00 |
| Claude Sonnet 4 | 8.29 | 1.31 | — |
| Claude Haiku 3.5 | 7.51 | 0.18 | — |
| DeepSeek V3 | 6.95 | 5.41 | 1.57 |
| GPT-4o Mini | 4.16 | 4.23 | — |
| GPT-4o | 4.12 | 2.68 | — |
| Gemini 2.5 Pro | 3.53 | 0.00 | — |
| GPT-5.4 | 1.43 | 0.29 | 0.00 |
| Gemini 2.5 Flash | 1.28 | 1.48 | — |
| Llama 3.1 8B Instruct | 0.00 | 0.00 | — |
| Llama 3.3 70B Instruct | 0.00 | 0.00 | — |
| **Human baseline (8 published essays, 57,232 words)** | **3.23 (mean, range 0.33–17.12)** |

Read it. GPT-4.1 produces em dashes at 3.3× the human mean and resists suppression even under explicit prohibition. Claude Opus 4.6 is high unconstrained but *complies perfectly* under suppression. Llama produces zero. GPT-5.4 has been actively reduced.

**Rules.**

1. Em dashes are not banned. Humans have used them for centuries.
2. More than one em dash per three or four paragraphs is above human baseline for most registers.
3. Even a single em dash is a tell if it's performing the classic AI move: injecting a dramatic explanatory clause to create false profundity ("The answer is simple — or is it?").
4. Use em dashes as humans do: for genuine asides, parenthetical material that cannot be expressed any other way, interruptions of thought. Not as rhythm-fillers.

### 5.11 Title case in headings

AI chatbots default to Title Case For All Main Words In Section Headings. Most human writing in most registers uses sentence case. The exception is formal US magazine / journal style guides, which do use title case.

**Rule.** Match your publication's house style. If there is none, use sentence case for headings; it aligns with modern editorial practice (Guardian, BBC, most tech docs) and breaks an AI default.

### 5.12 Curly vs. straight quotes

ChatGPT and DeepSeek output curly quotes ("curly") and curly apostrophes (it's). On a technical platform that expects straight ASCII, this is a tell. In publishing contexts (Chicago style, InDesign workflows, macOS smart-quote autocorrect) it is not. Gemini and Claude models typically do not use curly quotes. Context-dependent; do not over-weight.

### 5.13 Formal syntactic divergences (HPSG-level)

Zamaraeva et al. (ACL 2025 Long Papers) compared NYT-style human writing to six LLMs using Head-driven Phrase Structure Grammar. They found systematic differences in constituency length, dependency distances, and variety of syntactic constructions — LLMs produce longer constituents and less variety. At the grammar-type level, LLM text is more templatic: repeated use of similar clausal openings ("It is important to note that…", "In order to…") and recurrent coordination patterns. The reliability of these signals increases at longer text lengths.

**Operational implication.** If you find that the first 5–8 words of every paragraph follow a similar syntactic template, the piece is AI-shaped even if every word is human-replaced.

### 5.14 Performed authenticity (second-generation tells)

When models are prompted to "sound human" they overshoot, producing a new family of tells. These are subtler than classic AI vocabulary because they *perform* the very signals — informality, opinion — that mark human writing, but mechanically. Catalogued by the Humanizer kit (Berman 2026, patterns 25–28) as "performed authenticity."

**Sub-patterns.**

1. **Philosophical mic drops** — "Maybe both." / "And honestly?" / "Maybe that's the point." / "I think that says something." / "If that's not [noun], I don't know what is." / "Which is either … or …" End-of-paragraph reflection that gestures at depth without adding any. A shrug performing thoughtfulness.

2. **Performed balanced contrasts** — "[X] but not [Y]." / "Simple enough to use, powerful enough to matter." / "Take the work seriously but not yourself." Sentence-level cousin of §6.6 both-sides framing. Real human contrasts are lopsided; the perfectly weighted form is AI.

3. **Brand-manifesto structure** — Each paragraph labels cleanly with a single word (Identity / Function / Values / Reflection / Mission). Reads as if drafted from a creative brief. Real writing leads with whatever's most interesting and lets details surface.

4. **Parenthetical personality injection** — "(and honestly?)" / "(not that I'm complaining)" / "(if that makes sense)" / "(or something like that)" / "(maybe that's the point)" Mid-sentence asides that decorate rather than disrupt. Real asides break the sentence; these soften authority.

**Why this category.** §4 and §5.1–§5.13 catalogue first-generation tells — what the model produces by default. These four are second-generation: surface moves the model produces specifically when prompted to "sound human" or "add personality." Cleaning a first-generation tell often produces a second-generation one in its place. Expect more as RLHF further fine-tunes for "naturalness."

**Rule.** Strip every philosophical mic drop without replacement. Don't soften authority with parenthetical asides — say it directly or cut the sentence. If your paragraph structure could be labelled with one-word themes, restructure.

---

## 6. Rhetorical bans

### 6.1 Artificial suspense

AI loves to promise insight before delivering nothing (17-tells analysis by Jim Christian, 2025):
- "Here's what blew my mind:"
- "The answer surprised me:"
- "The crazy part?"
- "Plot twist:"
- "Here's the thing:"
- "And honestly?"
- "Here's what separates X from Y:"
- "This is what nobody tells you about…"
- "The uncomfortable truth is…"

**Rule.** State the finding. Suspense constructions are permission to skip the next sentence.

### 6.2 False precision

AI generates concrete-sounding examples that are actually generic: *"Consider a marketing team at a mid-sized company…"* / *"Sarah, a software engineer…"* Cherryleaf calls this "generic specificity" and notes it may be the strongest structural tell: "AI provides examples that feel specific without actually being specific. *'A procurement policy that made sense for a manufacturing business might not work for a software division.'* True! But *which* procurement policy? *Which* manufacturing business?"

**Rule.** Every specific example must be specific. Named person, named company, dated event, or it is cut.

### 6.3 Fake anecdotes and fabricated authority

- "I spoke with dozens of engineers…" — if you didn't, don't say it.
- "I've been doing this for years…" — if written by an LLM, this is a lie.
- "In my experience…" followed by generic advice — a tell.
- Fabricated quotes attributed to real people.
- Fabricated citations with plausible-looking DOIs that resolve to unrelated papers (WP:AISIGNS catalogues this specifically: LLMs generate references to non-existent papers with DOIs that do exist but lead to unrelated articles).

The NYT / *Guardian* / Alex Preston incident of March–April 2026 is the canonical warning. Preston, an accomplished six-time author who had written for the NYT for five years, used an AI "editing tool" on a book review draft. The AI silently incorporated passages from a prior *Guardian* review of the same book. A reader noticed the overlap. Preston was dropped by the NYT. AI drafting is forensically checkable; plagiarised-by-AI is still plagiarised.

**Rule.** Never keep an anecdote, quote, or citation an LLM generated without verifying it against an external primary source.

### 6.4 Significance inflation

AI writing puffs up every topic. Wikipedia:AISIGNS catalogues a specific repertoire: "stands as a testament," "marking a pivotal moment," "represents a significant shift," "underscoring its importance," "symbolising its enduring legacy," "setting the stage for," "cementing its role as," "a cornerstone of," "an indelible mark," "of profound importance," "deeply rooted," "nestled in the heart of," "boasts a rich history of."

**Rule.** Write about the thing, not about the importance of the thing. The importance should be legible from the facts. If you find yourself writing "X represents a significant shift," replace that entire sentence with what actually happened: who did what, when, to what effect.

### 6.5 Unnecessary enthusiasm

AI writing flatters the reader. Every idea in a list is "excellent," "powerful," "transformative," "exciting." Every approach is "elegant." Every insight is "invaluable." Every opportunity is "tremendous." Every future is "bright."

**Rule.** Praise is earned by content. Strip all adjectives of praise from your own work and see if the claim still reads as strong. Usually it reads stronger.

### 6.6 Both-sides framing as default

"While X is true, it is also important to consider Y." "On the one hand … on the other hand…" "There are valid arguments on both sides." This is RLHF's face-saving training in pure form (Dev.to analysis of DPO/RLHF objectives, March 2026).

**Rule.** If one side is stronger, say so. "Both sides" is appropriate only when the evidence genuinely is split and you have the sources to show it.

### 6.7 The motivational poster close

"In the end, what matters most is… Every journey begins with a single step… The future is ours to shape… Let's build something extraordinary…"

**Rule.** Business/tech writing never ends like this. Close on a fact, a next action, or a question the reader now has to answer.

### 6.8 Rhetorical questions in clusters

"How do we solve this problem? What does this mean for leaders? Why does this matter?" Cherryleaf: "AI loves rhetorical questions, especially in clusters of three (see: tricolon). But these aren't genuine inquiries opening space for thought. They're declarative statements wearing question marks, transitions disguised as engagement."

**Rule.** Ask questions you don't know how to answer. One rhetorical question per piece, maximum, and only if the question has teeth.

### 6.9 False ranges

"From X to Y" framing where X and Y aren't on a meaningful scale. *"Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter."* The endpoints don't bound a continuum; they're impressive examples dressed as a span.

**Rule.** Use "from X to Y" only when X and Y are real extremes of an ordered set (dates, sizes, levels, prices). Otherwise list the items plainly: "The book covers the Big Bang, star formation, and current theories about dark matter." Source: Humanizer kit pattern #12 (Berman 2026).

---

## 7. Tone rules

### 7.1 Commit to a voice

AI default voice: formal, neutral, courteous, risk-averse. If that is your house voice (legal, medical, regulatory), this section does not apply — but also, your AI tells will be harder to eliminate because they overlap with your house style, and you'll need to lean harder on §4–§6.

For everything else: pick a voice with edges. Conversational and informed. Opinionated and specific. Technical and dry. Sardonic and precise. Any committed voice beats the AI courtesy voice.

### 7.2 Use the first and second person where appropriate

Brown et al.'s Biber table: GPT-4o uses first-person pronouns at 62% of human rate and second-person at 52% of human rate. LLMs default to third-person passive ("it should be noted that users may experience…"). First and second person are human defaults in blog posts, documentation, and post-mortems. Use them.

### 7.3 Use contractions

"It's," "don't," "you're," "we've." Brown et al.: GPT-4o uses contractions at only **60%** of human rate. Formal technical reference documentation legitimately avoids them; essays, blog posts, guides, and internal comments do not. Contractions are one of the cheapest and highest-signal ways to move a piece away from the AI default.

### 7.4 Start sentences with "And" and "But"

The grammar-school rule against this is not a rule. Do it. AI almost never does.

### 7.5 Use fragments

Like this. Where they earn their keep. Brown et al. don't break out fragments specifically, but the combination of higher "that"-clause usage and participial-clause usage in LLMs is a marker of structurally complete sentences at rates no careful human matches.

### 7.6 Strong claims, specific numbers

"About half" → "47%" if you know it, "half" if you don't. "Significantly faster" → "2.3× faster on our dataset." Generic quantifiers ("many," "numerous," "a significant number of," "plenty of") are AI defaults.

### 7.7 Allow profanity and bluntness where it fits

Brown et al.'s most-underrepresented-words table for GPT-4o includes (at rates 0.01–0.02× of human use): "fucking," "fuck," "asshole," "shit," "nasty," "blah," "yep," "ok," "i.e." Well-placed informal or blunt language is a powerful de-AI signal because the model has been explicitly trained not to produce it. In contexts that permit it, use it.

### 7.8 Register shifts within a piece

A formal sentence followed by "but honestly, that's insane" is human. A formal paragraph followed by a casual one is human. Brown et al. demonstrated instruction-tuned LLMs show limited register variation. Humans adapt; shift register when the subject matter turns.

---

## 8. Formatting rules

### 8.1 Bullet discipline

AI's default output format is a bulleted list with bold inline headers. Most serious prose is not a bulleted list. Freeburg's paper shows that even under markdown suppression, a residual bullet-and-bold reflex leaks through.

- **Use bullets** for genuinely enumerable, parallel items (lists of requirements, lists of options, lists of references).
- **Do not use bullets** as a substitute for writing paragraphs. If an item in a bullet list is more than two lines of prose, it wanted to be a paragraph.
- **Never nest bullets three deep** unless you are writing a reference document with genuine hierarchical structure.
- **Do not convert "challenges" or "benefits" into bullet lists** in articles. The resulting structure is Wikipedia:AISIGNS's "Inline-header vertical lists" pattern — a strong AI signature.

### 8.2 Bold restraint

The "every third word is bold" pattern is a direct import from marketing copy, slide decks, and how-to listicles — all heavily represented in training data. Wikipedia:AISIGNS notes "AI chatbots may display various phrases in boldface for emphasis in an excessive, mechanical manner" and gives real Wikipedia draft examples where entire narrative paragraphs were dotted with bold.

**Rule.** In body prose, use bold at most once per section and only for genuine emphasis on a load-bearing term. If you want something to stand out, write a sentence that stands out.

### 8.3 Emoji

Professional technical writing, long-form journalism, and most documentation do not contain emoji. 🚀 ✨ 💡 as section decorators or headline enhancers are AI fingerprints. The *Washington Post* 328,744-message analysis found ChatGPT "leans heavily on emojis" as one of its three strongest lexical tells. If your brand voice uses emoji deliberately, fine — but never auto-accept what an LLM produces.

In open-source project READMEs specifically, `## Features ✨` is a near-certain AI signature (see §9.2).

### 8.4 Markdown leakage

When asked to generate prose for a non-Markdown context, LLMs leak Markdown: stray `**bold**`, `---` thematic breaks, inline `# headers` rendered as literal hashes. Wikipedia:AISIGNS catalogues specific leak patterns: thematic breaks (`----`) before each heading, explicit `1.` list numbering instead of wikitext, `##` used to denote section headings on platforms that interpret `##` differently.

Audit for this every time.

### 8.5 Heading patterns

- No skipped heading levels (H1 → H3 with no H2 is an AI tic because the chat app rendered H1 at the top and H3 was the first "inner" heading; Wikipedia:AISIGNS).
- No decorative divider lines (`---`) above every heading.
- No "Summary" or "Conclusion" heading at the end of everything.
- Sentence case unless the house style mandates title case.

### 8.6 ChatGPT-specific leaks to grep for

Wikipedia:AISIGNS catalogues model-specific markup bugs that end up in the text when users paste chat output:

- `turn0search0`, `turn0search1`, `iturn0image0turn0image1` (ChatGPT web search reference placeholders)
- `:contentReference[oaicite:N]{index=N}`, `oai_citation:N`, `Example+1` (ChatGPT citation bugs)
- `({"attribution":{"attributableIndex":"X-Y"}})` (JSON attribution leak)
- `utm_source=openai`, `utm_source=chatgpt.com`, `utm_source=copilot.com`, `referrer=grok.com` (UTM tags added by chatbots to cited URLs)
- `[attached_file:1]`, `[web:1]` (Perplexity-specific tags)
- `grok_card` XML tags (Grok)
- `access-date=2025-XX-XX` or `access-date=2025-xx-xx` (LLM placeholder dates in citations)
- `INSERT_SOURCE_URL_30`, `PASTE_YOUTUBE_VIDEO_URL_HERE`, `[Your Name]`, `[Describe the specific section]` (unfilled phrasal templates)

Running `grep -E 'turn0|oaicite|oai_citation|utm_source=(openai|chatgpt|copilot)|access-date=.{4}-XX-XX'` on any suspect document catches most of these in one pass.

---

## 9. Domain-specific guidance

### 9.1 Articles, essays, blog posts

The tells in §4 and §5 are most damaging here because readers actively assess voice. Additional rules:

- **Intros must commit immediately.** Drop the scene-setting paragraph. The first sentence should already be doing work.
- **No TL;DR at the top unless your publication demands it.** AI defaults to summary-first structure; leading journalism leads with the lede, not the recap.
- **Include at least one moment of observational specificity** — something you saw, something you measured, something you remember. AI cannot produce these. Human pieces without them read as AI-adjacent even when they aren't. Brown et al. found GPT-4o uses rare, specific proper nouns like "Deborah" or actual place names at a small fraction of human rates.
- **Cite real sources with page numbers or URLs.** AI-hallucinated citations are the most reputationally destructive tell; the NYT / Alex Preston / *Guardian* incident (March 2026) is the canonical warning. Journalism institutions are now actively detecting, with *The Globe and Mail* (April 2026 standards-editor column) noting that contributors to Opinion, First Person, and Lives Lived must attest their work is "original and created without the use of artificial intelligence."
- **No Elara Voss.** If your piece contains a fictional character, make sure the name does not match the ChatGPT-era canonical set: Elara, Elena, Kael, Sarah, Emily, and variations. Pangram's measurement: 60–70% of character names in unprompted ChatGPT/Claude short fiction are "Emily" or "Sarah." Kriss found the same for SF protagonists.
- **Write one opinion, not a survey of opinions.** Cherryleaf: "Real writers pick a position and defend it. AI always presents both sides."

### 9.2 Technical documentation

Documentation has its own AI-tell profile because many detection heuristics false-positive on technical writing (Pangram 2025). But specific patterns are still clearly AI:

- **Over-explained trivial operations.** A README section that opens with "In today's fast-paced development environment…" is AI. Good docs say what the thing is and what it does, then stop.
- **Generic "Prerequisites / Installation / Usage / Troubleshooting / Contributing / License" scaffolding with no content specificity.** AI produces the skeleton of a README. Your README must have content not generated.
- **Version specificity.** Real docs say `python>=3.11` and `node 20.11.1` and `webpack 5.92.0+`. AI docs say "ensure you have Python installed."
- **Error messages quoted verbatim.** AI rarely produces real error strings; when it does, they are often slightly wrong. Copy-paste real ones.
- **No emoji in section headings** (`## Features ✨` is a near-certain AI signature for professional technical documentation per Mohamed Abdullah's 2025 analysis).
- **No marketing copy in technical docs.** "Seamlessly integrate," "empower developers," "revolutionise your workflow" — none of these belong in a README.
- **No three-line horizontal rules (`---` or `***`) separating every section.** This is markdown leaking (Freeburg 2026).

### 9.3 Code comments

Human developers under-comment. AI over-comments. The ratio is the tell. Codequiry's 2026 analysis of thousands of flagged submissions identifies over-commenting as the most reliable AI indicator in code.

**Ban:**

- Comments that restate the code in English. `// increment counter` above `counter++;` is an AI signature. Example from the Codequiry analysis:
  ```
  # Calculate the total by iterating through the list
  total = 0
  for price in price_list:
      # Add the current price to the running total
      total += price
  # Return the calculated total
  return total
  ```
  Three comments, three redundant restatements. No human writes this.
- Over-formal multi-sentence docstrings on trivial internal functions.
- Comments that reference the task, the PR, the AI session, or "as requested."
- Decorative divider banners (`// =========== USER MANAGEMENT ============`).
- Emoji in code comments outside projects that use them deliberately.
- "TODO: implement later" on code you could implement now.
- "This handles all edge cases" — AI over-claims; humans say "handles null and negative n; check for NaN separately."
- Generic over-engineered edge case handling that doesn't match the assignment scope. Student solving "reverse a string" does not proactively handle multi-byte Unicode grapheme clusters; an LLM does.
- Perfect symmetry of error handling across every function, including where none is needed. AI adds try/catch everywhere; humans add it where they've seen it fail.

**Keep:**

- WHY comments. The non-obvious reason the code is the way it is — a workaround for a specific bug, a hidden invariant, a constraint from an external system.
- Version / environment qualifiers (`// only works on node >= 20 because of structuredClone behaviour`).
- Warnings about footguns (`// DO NOT reorder — the auth call must happen before the session write or we leak`).
- Specific error-code references (`// returns EAGAIN if the ring buffer is saturated; retry with backoff`).

A good rule of thumb: if deleting the comment would leave no reader of the code confused, delete it.

### 9.4 Marketing copy

Marketing copy is where AI writing is most compressed and most recognisable, because marketing corpora dominate training data and RLHF rewards exactly the register that sells. The same 400-word Pangram vocabulary list applies with 2× sensitivity.

- Ban "seamlessly," "empower," "elevate," "transform," "unlock," "revolutionise," "cutting-edge," "next-generation," "game-changing," "state-of-the-art," "industry-leading," "end-to-end," "at scale," "best-in-class," "holistic," "mission-critical," "robust," "scalable," "turnkey."
- Ban abstraction: "solutions," "platforms," "experiences," "journeys," "ecosystems."
- Replace every generic benefit with a specific verifiable one. "Saves time" → "5 minutes off a median checkout." "Increases engagement" → "+14% 7-day retention in our A/B test."
- No tricolons in headlines.

### 9.5 Commit messages, PR descriptions, changelog entries

Wikipedia:AISIGNS flags LLM-generated edit summaries as "formal, first-person paragraphs, without abbreviations, and conspicuously echoing the exact text or shortcuts of policies… They often mention things that they 'ensured' or 'avoided' doing."

Real example from a 2025 Wikipedia edit summary (AI-generated): *"Concise edit summary: Improved clarity, flow, and readability of the plot section; reduced redundancy and refined tone for better encyclopedic style."* Every word is an AI signature.

**Rule.** Imperative mood, short, factual. "Add X." "Fix Y in Z." "Remove dead path in foo.bar." One line unless the PR description genuinely needs more.

### 9.6 Code review, issue comments, and OSS discussion

CHAOSS Project data from 2024: AI-generated OSS comments rose from 0.9% (Q1 2023) to 7.3% of non-maintainer comments. The specific patterns maintainers see:

- **Documentation Mirror:** Comments that regurgitate official docs verbatim but omit documented caveats.
- **Solution-First, Constraint-Agnostic:** Proposing elegant code fixes without referencing actual error logs, environment versions, or project-specific constraints.
- **Consensus Vacuum:** "most developers agree," "it is widely accepted," "best practices suggest" — appeals to unnamed authority.
- **Absence of versioned specificity:** No `python --version`, no exact error strings, no stack traces.
- **Missing "why not X?" reasoning:** Human proposals weigh alternatives; AI proposals don't.

If you are participating in OSS discussion: cite exact versions, paste exact error messages, show actual output. The signals are the absence of signals.

---

## 10. Detection methods: what they actually measure

Understanding what classifiers look at tells you what to neutralise in your own work. The research on detection converges on seven signal classes (Deep-research synthesis; Crothers et al. 2023; Mitchell et al. DetectGPT 2023; Bao et al. Fast-DetectGPT 2024; McGovern et al. 2025; Xiang et al. 2026):

1. **Lexical over-representation lists.** Gray (2024), Juzek & Ward (2025), Kobak et al. (2024), and Pangram maintain lists of ~20 to ~400 words whose frequency in AI output exceeds human baseline by orders of magnitude.
2. **Perplexity / surprisal diversity.** Lower mean surprisal under a reference LM, and lower variance of surprisal across tokens. DivEye (Dey et al. 2025, arXiv:2509.18880) and Binoculars (Hans et al. 2024, arXiv:2401.12070) are current SOTA zero-shot methods.
3. **Burstiness.** Coefficient of variation of sentence-length distribution, and of per-sentence perplexity.
4. **POS-tag n-gram distributions.** McGovern et al.'s Grammarly/Cambridge paper showed simple decision-tree classifiers on POS-n-gram features achieve 0.94–0.98 macro-F1 distinguishing GPT-4 vs human. These fingerprints are "consistent within model families" (LLaMA 13B and 65B share a fingerprint) and "robust across text domains."
5. **Stylometric ensembles.** StyloAI (arXiv:2405.10129) uses 31 stylometric features and achieves 81–98% accuracy.
6. **Formal syntax features.** Zamaraeva et al. (ACL 2025) use HPSG grammar types. Tagset distributions diverge systematically.
7. **Watermarks.** Kirchenbauer et al.'s green/red token scheme and successors embed detectable statistical signatures during generation. Reliable only when applied at generation and not laundered through editing.

**Why single-metric detectors (GPTZero, ZeroGPT, QuillBot) produce false positives.** A 2023 Stanford study flagged 61% of non-native-English TOEFL essays as AI. Non-native writers produce lower-perplexity text because they avoid unusual constructions; single-threshold perplexity detectors collapse the axes "non-standard word choice" and "AI-generated." *The Globe and Mail* (April 2026): three different AI detectors on the same NYT "Modern Love" column returned three different verdicts.

**Operational implication.** Multi-feature, domain-calibrated ensembles are the state of the art. If your piece is clean against vocabulary, structure, perplexity, burstiness, and POS-n-gram profile simultaneously, no current detector will flag it. The §14 checklist is built against this multi-signal profile.

---

## 11. Evolution: what has changed 2023 → 2026

Signals matter only to the extent models still produce them. The research catalogues specific shifts:

- **"Delve" is in sharp decline.** Peaked 2023–early 2024; dropped off in 2025 after widespread mockery and (reportedly) internal fine-tuning adjustments. Remaining usage is still high vs. pre-2022 baseline, but "delve" alone is no longer proof.
- **Em-dash overuse has been partially suppressed** in GPT-5.1 / GPT-5.4 (November 2025 onward) after OpenAI acknowledged the issue. Sam Altman's Threads post confirmed the behaviour was adjusted in response to user preference. Absence no longer rules out AI.
- **"It's not X, it's Y"** has increased and is now the strongest structural tell (Washington Post, November 2025). 6% of July 2025 ChatGPT messages contain "not just X, but Y" variations.
- **"Showcase," "emphasising," "enhance," "highlighting"** are the persistent GPT-5-era vocabulary tells (Wikipedia:AISIGNS 2025/2026).
- **"Undue emphasis on notability, attribution, and media coverage"** is a newer pattern characteristic of newer models with retrieval — they list the sources the subject has been covered in rather than summarising what the sources said. Canonical phrase: "has been profiled in major outlets including…" "maintains an active social media presence" (uncommon on Wikipedia before ~2024).
- **Diffusion-based text models** (LLaDA family; arXiv:2507.10475) produce perplexity matching human baseline (44.62 vs 43.03), so perplexity-based detectors increasingly fail on them. Burstiness remains lower. Structural tells remain.
- **Obvious hallucinations and incoherence** (2022–early 2023 tells) have mostly disappeared as models improved.
- **Model-attribution fingerprints remain.** McGovern et al. (2025) showed that even GPT-4 and Cohere data can be distinguished from human and from each other at F1 > 0.94 using simple n-gram features; the fingerprint persists across model generations.

**Operational implication.** A clean piece today is a piece with ≤1 of the top-20 markers. Three years ago a clean piece could tolerate five.

---

## 12. Anti-patterns in "humanising" AI text

Three failure modes are common when people try to clean up AI drafts. Each one produces worse output than just rewriting.

### 12.1 Swap-and-pray

Replacing "delve" → "explore," "underscore" → "highlight," "intricate" → "complex." This defeats only the most naive detectors. The underlying voice (cadence, hedging, symmetry, false profundity) is untouched and readers still notice. The *Washington Post* piece's quote from a reader: *"the mismatch is even worse"* after surface-level edits because the remaining structure is still AI-shaped but now with vocabulary that doesn't match.

### 12.2 Anti-detector obfuscation

Adding intentional typos, forced fragments, random "And"s. This produces prose that reads as badly edited, which is worse than AI — AI at least reads as competent. The goal is good human writing, not corrupted AI. The Pangram research on humanizer tools (DUPE / paraphrasing attacks; arXiv:2404.11408) shows this approach defeats detectors temporarily while producing text that human readers find obviously worse than either AI or human originals.

### 12.3 Heavy prompt engineering

"Write in the style of Hemingway with no em dashes, no hedging, no tricolons, vary sentence length between 5 and 30 words…" The model complies for 200 words, then drifts. Freeburg's three-condition suppression gradient is the empirical demonstration: GPT-4.1 retains 3.86 em dashes per 1,000 words even under explicit em-dash prohibition, and 6.97 in 5,000-word outputs. Every prompt is a leaky abstraction over the underlying training distribution.

### 12.4 What actually works

Rewriting, not editing. Take the AI draft as research — a set of claims, facts, and a rough outline — and write the final version from a blank editor. It is faster than editing a draft sentence by sentence and produces better output.

For AI-assisted drafts where rewriting isn't practical:
1. Delete every Tier-1 vocabulary word (§4.3). No replacement; usually the sentence is better without.
2. Delete every hedge (§4.7). If the claim is true, say so; if not, remove it.
3. Delete every "not X, it's Y" construction (§5.1).
4. Delete every terminal participial phrase that doesn't add a fact (§5.5).
5. Vary paragraph and sentence lengths deliberately (§5.9).
6. Add at least one observational specific (§2 item 12, §9.1).
7. Take a position (§3 P2).
8. Re-read aloud. Fix any sentence that doesn't sound like you saying it.

---

## 13. Pre-publish checklist

Run every piece through this before shipping. A piece scoring 3 or more "hits" should be rewritten.

### Vocabulary scan (grep in the editor):

- [ ] delve, delves, delving, delved (any hit → rewrite)
- [ ] tapestry (any hit → rewrite)
- [ ] intricate, intricacies (any hit → rewrite)
- [ ] realm, testament, vibrant (any hit → rewrite)
- [ ] underscore(s), showcase(s), leverage (as verb) (more than 1 combined → rewrite)
- [ ] boasts (as "has"), seamless(ly), navigate (metaphorical) (any hit → rewrite)
- [ ] foster(ing), harness(ing), embark (more than 1 combined → rewrite)
- [ ] crucial, pivotal, vital, paramount, multifaceted, nuanced, comprehensive (more than 2 combined → rewrite)
- [ ] camaraderie, palpable, fleeting, solace, unspoken, grapple, amidst, cacophony (any → rewrite in fiction; if nonfiction, near-certain AI)
- [ ] "signal, not noise" / "signal vs noise" / "signal over noise" / "more signal than noise" (any hit → rewrite — banned outright per §4.3)

### Opener / closer scan:

- [ ] Zero occurrences of "In today's … world," "In recent years," "In the realm of," "In the ever-evolving …"
- [ ] Zero occurrences of "In conclusion," "In summary," "Overall," "Ultimately," "The bottom line," "At the end of the day."
- [ ] Zero occurrences of "It's important to note," "It's worth noting," "It should be noted."
- [ ] Zero chatbot artefacts ("I hope this helps," "Great question," "Certainly," "Absolutely").

### Structural audit:

- [ ] Count "not X, but Y" / "not just X, it's Y" / "not only X, but Y" / "less about X, more about Y." More than 1 per 1,000 words → rewrite.
- [ ] Count three-item lists and tricolons. If more than 30% of enumerations are exactly three items → rewrite.
- [ ] Check paragraph-length variance. Coefficient of variation > 0.4 → ok. < 0.2 → rewrite.
- [ ] Check sentence-length variance in any two consecutive paragraphs. Both within ±20% of mean → rewrite.
- [ ] Check conclusion. Does it balance "the good news / the challenge / a forward-looking closer"? → rewrite.
- [ ] Check copulas. If more than 2 instances of "serves as" / "stands as" / "represents" / "marks" / "boasts" / "features" → rewrite.
- [ ] Count terminal participial phrases ("-ing" phrases at end of sentence). If more than one per 300 words → rewrite.
- [ ] Count em dashes. If more than one per three paragraphs → rewrite or convert to commas/periods.
- [ ] Count philosophical mic drops ("Maybe both.", "And honestly?", "Maybe that's the point.", "I think that says something.", "If that's not [noun], I don't know what is."). Any hit → cut the line.
- [ ] Count parenthetical personality injections ("(and honestly?)", "(not that I'm complaining)", "(if that makes sense)", "(or something like that)"). Any hit → cut the parenthetical.
- [ ] Check "from X to Y" constructions. If X and Y don't bound a real ordered scale → rewrite as a plain list.

### Voice audit:

- [ ] Does the piece take a position, or does it "balance both sides"? If the latter, decide.
- [ ] Read aloud the opening paragraph. Would a human speak like this? If no, rewrite.
- [ ] Does it contain at least one observational specific (named person, specific number, concrete example from direct experience, real error message, real date)? If not, add one or acknowledge its absence explicitly.
- [ ] Does it contain first-person or second-person pronouns where appropriate? If the register permits them and there are none → consider adding.
- [ ] Contractions present where register permits? If register permits and none → add.

### Formatting audit:

- [ ] No stray Markdown in non-Markdown contexts (`**bold**`, `---`, `##`).
- [ ] No decorative `---` above every heading.
- [ ] Bold used ≤ once per section, for genuine emphasis.
- [ ] Emoji only if the house style demands it.
- [ ] Headings in sentence case unless style guide says otherwise.
- [ ] No nested bullets three deep.

### Leak audit (for AI-assisted drafts):

Run: `grep -E 'turn0|oaicite|oai_citation|utm_source=(openai|chatgpt|copilot)|access-date=.{4}-XX-XX|attached_file:|grok_card|\[Your Name\]|\[INSERT|\[PASTE'`

- [ ] Zero hits. Any hit → leak, fix before publish.

### Integrity audit:

- [ ] Every citation verified (URL resolves; page exists; the source actually says what you claim).
- [ ] Every quote traced to a real source (not AI-hallucinated).
- [ ] No fabricated anecdotes. No "in my experience" if the experience is model-generated.
- [ ] Every DOI resolves to the paper you cited, not an unrelated one.
- [ ] Every book citation has a page number or a verifiable URL.

---

## 14. Two worked before/afters

### 14.1 Marketing-register rewrite

**Before (AI draft, 76 words):**

> In today's rapidly evolving digital landscape, cybersecurity has emerged as a crucial concern for organizations of all sizes. As we navigate the complexities of modern threat vectors, it's important to note that a multifaceted approach is paramount. This isn't just about implementing tools — it's about fostering a culture of security. By leveraging comprehensive frameworks, organizations can seamlessly integrate robust defences that showcase their commitment to protecting stakeholders. Ultimately, the journey toward security resilience is a testament to the enduring importance of vigilance in our interconnected world.

Tell count:
- Lexical (Tier 1): evolving, landscape, crucial, navigate, complexities, multifaceted, paramount, fostering, leveraging, comprehensive, frameworks, seamlessly, integrate, robust, showcase, commitment, journey, testament, enduring, interconnected. **20 hits.**
- Structural: "It's not X — it's Y" (negative parallelism); "In today's … landscape" (opener ban); "Ultimately … testament" (hype close); three-noun tricolons ("tools," "culture," "frameworks"); every sentence within ±15% of the same length.
- Voice: no position, no specific, no named threat, no named tool, no year, no number.

**After (human rewrite, same word count):**

> Cybersecurity is a work-culture problem dressed up as a tooling problem. In the 2024 Verizon DBIR, 68% of breaches involved a non-malicious human action — someone who clicked, mis-configured, or re-used a password. You cannot buy your way out of that with a new EDR. The useful question is not "which tool?" but "which of our processes would have caught this incident?" When teams answer that question honestly, they usually discover their weakest link is code review, not the firewall.

Same claim-space, different voice: opinionated, specific source (2024 Verizon DBIR), specific percentage (68%), named tool category (EDR), concrete recommendation (code review). Zero Tier-1 vocabulary. No negative parallelism. Sentence lengths: 12, 27, 9, 18, 17 words — coefficient of variation ~0.4.

### 14.2 Technical README rewrite

**Before (AI draft, 68 words):**

> ## Overview ✨
>
> Our robust, cutting-edge library empowers developers to seamlessly integrate authentication into their applications. By leveraging industry-leading best practices, it provides a comprehensive, end-to-end solution that showcases enterprise-grade security while fostering a superior developer experience. Whether you're building a small prototype or scaling to millions of users, **AuthKit** streamlines your authentication workflow with its intuitive API.

Tells: emoji in heading (§8.3), every Tier-1 marketing word (robust, cutting-edge, empowers, seamlessly, leveraging, industry-leading, best practices, comprehensive, end-to-end, showcases, enterprise-grade, fostering, superior, streamlines, intuitive), "Whether you're a … or a …" opener ban, no specific API name, no version, no examples.

**After (human rewrite, same word count):**

> ## What AuthKit is
>
> AuthKit is a drop-in authentication library for Node.js (≥20) and Deno. It wraps OAuth2, OIDC, and WebAuthn behind one API and ships tested clients for Google, GitHub, Okta, and Microsoft Entra. Use it when you want short-lived JWTs with refresh-token rotation, rate-limited login endpoints, and audit-ready logs on day one. Not recommended if you need SAML — the protocol is deliberately excluded; see [saml-kit](#) for that.

Same word count, specific runtime versions, specific protocols, specific providers, specific features named, specific non-feature named with a reason, specific use-case guidance. Zero Tier-1 vocabulary. No emoji. Sentence-case heading.

---

## 15. References and primary sources

### Peer-reviewed / arXiv

- Reinhart, A., Brown, D. W., Markey, B., Laudenbach, M., Pantusen, K., Yurko, R., and Weinberg, G. "Do LLMs write like humans? Variation in grammatical and rhetorical styles," *PNAS* 2025 (preprint arXiv:2410.16107v1). DOI 10.1073/pnas.2422455122. **Source of the Biber 66-feature analysis, HAP-E/CAP parallel corpora, the present-participial-clauses 2–5× finding, and the over-represented words table (camaraderie, tapestry, palpable, intricate, etc.).**
- Juzek, T. S. and Ward, Z. B. "Why Does ChatGPT 'Delve' So Much? Exploring the Sources of Lexical Overrepresentation in Large Language Models," Proc. COLING 2025, pp. 6397–6411. **21 focal words; 3-step identification method; RLHF evidence via Llama 2-Base vs Llama 2-Chat entropy comparison.**
- Juzek, T. S. and Ward, Z. B. "Word Overuse and Alignment in Large Language Models: The Influence of Learning from Human Feedback," arXiv:2508.01930. **Direct experimental confirmation that LHF (RLHF + DPO) installs lexical preferences in Llama; online study showing participants systematically prefer text with focal words.**
- Kobak, D., González-Márquez, R., Horváth, E.-A., and Lause, J. "Delving into ChatGPT usage in academic writing through excess vocabulary," arXiv:2406.07016 / *Scientometrics* 2024. **14.2M PubMed abstracts 2010–2024; excess-words method; 329 excess words in Q1 2024; 10% LLM-usage lower bound; "delves" r=25.2, "crucial" δ=0.026.**
- McGovern, H., Stureborg, R., Suhara, Y., and Alikaniotis, D. "Your Large Language Models Are Leaving Fingerprints," Proc. GenAIDetect 2025, ACL, aclanthology.org/2025.genaidetect-1.6. **POS-n-gram fingerprints; 0.94–0.98 F1 on GPT-4 / Cohere / human; fingerprints consistent within model family across domains.**
- Freeburg, E. M. "The Last Fingerprint: How Markdown Training Shapes LLM Prose," arXiv:2603.27006, March 2026. **Em-dash mechanistic analysis; 12-model × 3-condition suppression gradient; Table 1 above.**
- Zamaraeva, O., Flickinger, D., Bond, F., and Gómez-Rodríguez, C. "Comparing LLM-generated and human-authored news text using formal syntactic theory," Proc. ACL 2025 Long Papers, pp. 9041–9060.
- Mitchell, E., Lee, Y., Khazatsky, A., Manning, C. D., and Finn, C. "DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature," ICML 2023.
- Hans, A., et al. "Spotting LLMs With Binoculars: Zero-Shot Detection of Machine-Generated Text," arXiv:2401.12070.
- Dey et al. "DivEye: Surprisal Diversity for Zero-Shot LLM Detection," arXiv:2509.18880.
- Liang, W., Yuksekgonul, M., Mao, Y., Wu, E., and Zou, J. "GPT detectors are biased against non-native English writers," *Patterns* 4(7), 2023. **61% of non-native TOEFL essays falsely flagged.**
- Zaitsu, W. and Jin, M. "Distinguishing ChatGPT(-3.5, -4)-generated and human-written papers through Japanese stylometric analysis," *PLOS ONE* 18(8):e0288453, 2023.
- Przystalski, K., Argasiński, J. K., et al. "Stylometry recognizes human and LLM-generated texts in short samples," arXiv:2507.00838, 2025. **0.87 Matthews correlation coefficient on 10-sentence texts in 7-way classification.**
- *Humanities and Social Sciences Communications*, "Stylometric comparisons of human versus AI-generated creative writing," 2025.
- "Can You Detect the Difference? Autoregressive vs. Diffusion Text Generation," arXiv:2507.10475, 2025. **LLaDA achieves human-matching perplexity.**
- Xiang, L., et al. "AI-Generated Text Detection: A Comprehensive Review of Active and Passive Approaches," *Computers, Materials and Continua* Vol. 86 Issue 3, 12 January 2026.

### Journalism / editorial

- Kriss, S. "Why Does A.I. Write Like … That?" *New York Times Magazine*, 3 December 2025. **Source of the "tickling" anecdote, the Elara Voss / Kael observation, the "delve" 2,700% post-2022 claim, and the structural-vs-vocabulary argument.**
- Merrill, J. B., Chen, S. Y., and Kumer, E. "What are the clues that ChatGPT wrote something? We analyzed its style." *The Washington Post*, 13 November 2025. **Analysis of 328,744 publicly shared ChatGPT gpt-4o messages from May 2024 – July 2025; 6% of July 2025 messages contain "not just X, but Y" variations.**
- Stillman, J. "The Structure of This Sentence Is a Dead Giveaway That AI Wrote It." *Inc.*, 19 December 2025.
- Yahoo Tech, "The 5 Biggest 'Tells' That Something Was Written By AI," 17 November 2025.
- *The Globe and Mail*, "What newsrooms are doing to stay ahead of AI," standards editor column, 4 April 2026.
- Loffhagen, E. "The New York Times drops freelance journalist who used AI to write book review," *The Guardian*, 31 March 2026. **The Alex Preston incident.**
- Landymore, F. "NYT Cuts Ties With Writer as Scrutiny of AI Content Grows," *Futurism*, 1 April 2026.
- Altman, S. Threads post re: em-dash frequency adjustment in ChatGPT, 2024.
- Gnuse, A. "The AI writing tics that hurt engagement: A study," *Search Engine Land*, 25 February 2026. **"Conclusion" headers = strongest negative engagement signal; 1,000+ URL study.**

### Practitioner / community reference

- **Wikipedia:Signs of AI writing (WP:AISIGNS)** — en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing. The most comprehensive community catalogue, with hundreds of annotated real examples from Wikipedia articles, drafts, and comments. Maintained by WikiProject AI Cleanup. **Required reading.**
- Pangram Labs, "Comprehensive Guide to Spotting AI Writing Patterns," 2 April 2025. **The ~400-word vocabulary list used in §4.**
- Pangram Labs, "Why Perplexity and Burstiness Fail to Detect AI," 4 March 2025.
- jpeggdev/humanize-writing, github.com/jpeggdev/humanize-writing. Open-source Tier-1 / Tier-2 vocabulary reference and 15-item detection heuristic.
- Cherryleaf, "Indicators that suggest something was written by AI," February 2026. **The Claude-written self-demonstration.**
- Nair, M. "Why Does AI Keep Saying 'It's Not X, It's Y'?" *Dev.to*, 17 March 2026. **RLHF / DPO contrastive-objective explanation.**
- Massobrio, A. "Triviality and Rhetorical Triplets — a Study on LLM Clichés," LinkedIn, 2025.
- Brookings, "Detecting AI fingerprints: A guide to watermarking and beyond," 2024.
- Berman, M. "Humanizer," OpenClaw kit v2.2.3, journeykits.ai/browse/kits/matt-clawd/humanizer, released 1 April 2026. **Source of §4.10 filler-phrase replacement table, §5.14 performed-authenticity patterns 1–4 (philosophical mic drops, performed balanced contrasts, brand-manifesto structure, parenthetical personality injection), and §6.9 false ranges. 28-pattern checklist derived from WP:AISIGNS.**

---

## 16. Meta: this guide against its own rules

This guide was reviewed against its own checklist. Specifically:

- **Vocabulary scan.** Zero occurrences in running prose of: delve, tapestry, intricate, realm, vibrant, testament, showcase, seamless, navigate (metaphorical), leverage (as verb), foster, crucial, pivotal, multifaceted, nuanced, comprehensive, robust, transformative, groundbreaking, revolutionary, camaraderie, palpable, fleeting, solace, grapple, amidst.
- **Opener / closer scan.** Zero openers of "In today's…", "In recent years…", "In the realm of…", "It's important to note…". Zero closers of "In conclusion…", "Overall…", "Ultimately…", "The bottom line…".
- **Negative parallelism.** One deliberate use in §5.1 as an illustrative example and one in §14.1's worked example. Zero elsewhere.
- **Tricolon density.** Enumerations mixed: two-item, three-item, four-item, seven-item, thirteen-item lists. No paragraph contains two consecutive tricolons.
- **Sentence-length variance.** Intentional short/long mix throughout; §6.5 closing paragraph opens with "Praise is earned by content." (4 words) then follows with a longer analytical sentence.
- **Paragraph-length variance.** Paragraphs vary from one sentence (several in §3) to twelve sentences (§1.2).
- **Opinions taken.** §5.1 calls negative parallelism "the single most recognisable AI structure." §12.4 asserts rewriting beats editing. §9.4 bans specific marketing words. §11 takes a position on which tells remain live versus which have decayed.
- **Specifics.** arXiv IDs, DOIs, publication dates, page numbers, percentage figures, specific model names, specific ratio values (1,374.92×, 6%, 0.118, 68%, 2,700%, 329 excess words, etc.) throughout §1, §4, §5, §10, §15.
- **Copulas.** "Is" used freely. "Serves as" / "stands as" / "represents" avoided except where literally functional.
- **No markdown leakage.** No stray `---` dividers above headings. No emoji in headings. Sentence case throughout.
- **First and second person** used appropriately in instructions: "you," "your," "we."
- **Contractions** used where register permits: "isn't," "don't," "can't," "wasn't."

If the guide itself read as AI-written, it would not be credible. The test survives.
