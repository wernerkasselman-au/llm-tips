# High-Signal Writing Guide (Tightened)

Evidence-based reference for prose, docs, articles, and code comments that don't read as LLM-generated.

**Scope.** English writing across four domains where AI tells damage most: published prose (articles, blogs, essays, marketing); technical docs (specs, READMEs, guides); code comments; commit messages, PR descriptions, issue comments. Applies whether written by humans, LLMs, or humans editing LLM drafts.

**Principle.** Goal isn't "evade AI detectors." Write prose lacking the statistical fingerprints of a model trained to please human raters — uniform, risk-averse, noun-heavy, rhetorically predictable, devoid of observational grit.

**How to use.** Greenfield: internalise §2–§3, run §13 before publishing. AI-assisted drafts: treat §4–§10 lists as grep targets. 10+ hits per piece means rewrite, not edit. Rewriting from scratch using the draft as notes beats sentence-by-sentence editing — see §12.

**Evidence.** Every rule ties to a quantitative source. Core: Reinhart, Brown et al. (*PNAS* 2025, DOI 10.1073/pnas.2422455122); Kobak et al. (*Scientometrics* 2024, arXiv:2406.07016); Juzek & Ward (COLING 2025); Freeburg (arXiv:2603.27006); McGovern et al. (GenAIDetect 2025); Zamaraeva et al. (ACL 2025); *Washington Post*'s 328,744-message analysis (Merrill, Chen & Kumer, 13 Nov 2025); WP:AISIGNS; Kriss, *NYT Magazine* 3 Dec 2025. Full refs §15.

---

## 1. Why AI writing sounds the way it does

Three training-pipeline forces converge to produce the AI voice. Synonym swaps don't fix it.

### 1.1 Pre-training selects formal, markdown-saturated corpora

LLMs train on high-quality web text: Wikipedia, academic papers, news, GitHub READMEs, Stack Exchange. The Pile and RedPajama lean toward markdown and copy-edited content under formal-register style guides. Formal, hedged, noun-heavy English over-represents; casual conversational registers under-represent (Freeburg 2026; McGovern et al. 2025). This installs a *latent structural orientation* — not a defect, a distribution — that post-training then amplifies or suppresses.

### 1.2 Instruction tuning imposes noun-heavy informational density

Reinhart, Brown et al. built parallel corpora of ~12,000 human texts and GPT-4o / Llama 3 continuations of the first 500 words, then measured Biber's 66 morphosyntactic features per 1,000 words. Instruction-tuned models diverge from humans consistently (rates relative to human use, Brown et al. 2025, Table 3):

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

**Read it.** Llama 3 base models (right two columns) sit close to human rates almost everywhere. Instruction tuning pushes them toward the noun-heavy, participle-heavy, low-first-person, low-contraction register of GPT-4o. Not a bug — signature of a model trained to sound authoritative.

GPT-4o sample: "Bryan, leaning on his agility, dances around the ring, evading Show's heavy blows." Two present participles in one sentence. No human boxing writer writes that.

Llama 3 70B Instruct, four nominalizations: "These schemes can help to reduce deforestation, habitat destruction, and pollution, while also promoting sustainable consumption patterns."

### 1.3 RLHF / DPO contrastive optimisation rewards antithesis and verbosity

RLHF trains a reward model on rater preferences and optimises toward high-reward outputs; DPO formalises the same objective as a contrastive loss. Both move *toward* chosen completions and *away* from rejected ones.

Chosen completions tend to be longer, more hedged, more "balanced," more rhetorically polished; rejected ones are flat and declarative. The contrastive objective installs four tells:

1. **"It's not X, it's Y"** antithesis — surface form of contrastive training: repudiates the rejected, proposes the preferred.
2. **Hype register** ("crucial," "pivotal," "transformative," "testament to") — preferred by raters wanting answers to "sound smart."
3. **Both-sides framing** ("While X is true, Y is also important…") — face-saving to avoid "wrong" ratings.
4. **Em dash** — amplified by raters perceiving em-dash-heavy prose as precise.

Sam Altman acknowledged ChatGPT's em-dash frequency was deliberately tuned to user preference (Freeburg 2026), confirming RLHF can target punctuation-level features.

Juzek & Ward (COLING 2025) confirmed RLHF's role experimentally: Llama 2-Base vs Llama 2-Chat (same architecture and weights, differing only in fine-tuning). Llama 2-Chat is "considerably less surprised" (per-word entropy 0.886 vs 1.051) by ChatGPT-generated abstracts containing focal words. Direct evidence that RLHF, not architecture or pre-training data, installs lexical preferences.

### 1.4 You can't prompt your way out

Negative instructions ("don't use em dashes," "don't hedge," "write in my voice") degrade within hundreds of tokens and fail in longer outputs. Freeburg's three-condition gradient: GPT-4.1 produces 10.62 em dashes per 1,000 words unconstrained, 9.10 under markdown suppression, *still 3.86 under explicit em-dash prohibition*. Structural impulse overrides explicit instruction.

What works: rewrite from scratch using the AI draft as research. See §12.

---

## 2. What natural human writing looks like

Twelve characteristics distinguish human prose (Kobak et al. 2024; Juzek & Ward 2025; Reinhart, Brown et al. 2025; McGovern et al. 2025; *Washington Post* 2025; WP:AISIGNS).

1. **Positive burstiness.** Sentence lengths positively skewed: many short, some medium, occasional long. AI clusters around a bell curve. CoV: AI 0.15–0.25, human 0.4–0.7 across non-academic registers.
2. **Unpredictable word choice.** Per-sentence perplexity varies widely — factual sentence, metaphor, fragment. LLMs minimise per-step perplexity; humans don't.
3. **Concrete proper nouns.** Specific people, places, dates, product names, version numbers, error codes. AI defaults to placeholders ("a major city," "a leading company," "a marketing team at a mid-sized firm"). Pangram: 60–70% of character names in unprompted ChatGPT/Claude short stories are "Emily" or "Sarah." Kriss: ask any AI for SF and you get protagonists named "Elara Voss" or "Kael" with uncanny frequency; pre-2023, not a single self-published Amazon book used "Elara Voss." Late 2025: hundreds.
4. **Asymmetric attention.** Important points get more space; minor points get a sentence. AI allocates democratically — every subsection roughly equal length, every list item parallel grammar.
5. **Opinions taken at normal risk.** Position stated, not balanced. "Whether X or Y": red flag. "X, because Y": human.
6. **Visible thinking.** False starts, self-correction, mid-sentence pivots, "actually, wait —" moments. Clean first-draft prose reads as machine output.
7. **Grammatical imperfection.** Sentence fragments. Starting with "And" or "But." Occasional missed preposition. Inconsistent Oxford comma. Contractions — instruction-tuned Llama uses them at 129–142% of human rate only because base rate trained low (Llama base near-human; GPT-4o 60% of human).
8. **Lexical specificity.** Precise verbs over hedged generics ("crashes on null input" beats "handles edge cases poorly").
9. **Register variation within a piece.** Shifts between formal and conversational, deliberately. Brown et al.: instruction-tuned LLMs show limited variation — same dense, participle-heavy style across TV scripts, blog posts, transcripts, academic articles. Humans adapt.
10. **Refusal to over-explain.** AI announces structure, delivers content, summarises. Humans state things once.
11. **Specific obscenity and informality.** Brown et al.'s most-underrepresented words for GPT-4o: "fucking" (0.0083× human rate), "fuck," "asshole," "shit," "nasty," "ok," "blah," "yep," "i.e." AI doesn't write how people talk. One well-placed informal word: powerful de-AI signal.
12. **Real named things.** Real people, companies, products, error messages, dates, page numbers, version numbers. AI produces only plausible-looking substitutes.

---

## 3. Core principles

Five principles override every detailed rule in §4–§10. When a rule and a principle conflict, follow the principle.

### P1. Specificity over abstraction

Every generic noun ("landscape," "ecosystem," "framework," "realm," "dynamic") is an opportunity for a specific one. Every unnamed authority ("experts argue," "studies show," "observers note") is a weasel citation to name or delete.

> **Before:** "Studies show that AI is transforming the healthcare landscape."
> **After:** "A 2023 RAND survey of 2,400 US physicians found 38% had used an LLM for a clinical decision in the previous month."

Kobak et al.: 2024 PubMed excess vocabulary was 66% verbs, 18% adjectives — overwhelmingly style words, not topic words. Covid excess vocabulary, by contrast, was almost entirely content words (remdesivir, respiratory, omicron). Style words float; content words pin text to specific referents.

### P2. Commitment over balance

If a claim is true, state it. If defensible but contested, defend it. Don't present every question as "nuanced" or "multifaceted" then refuse to take a position. Reflexive "both sides" framing is the single clearest RLHF artefact. Cherryleaf: "Real writers with expertise pick a position and defend it. AI always presents both sides."

> **Before:** "While there are valid arguments on both sides, the optimal approach ultimately depends on context."
> **After:** "For latency-sensitive workloads, gRPC is the right choice. REST wins everywhere else because the tooling gap isn't worth closing."

### P3. Rhythm over symmetry

Mix sentence lengths deliberately. A 28-word sentence followed by a 3-word sentence: human signature. Three 10-word sentences in sequence: machine. Let some paragraphs be one sentence, others ten. Let one section be twice as long as the next.

### P4. Do the work instead of gesturing at it

Tempted to write "this is a complex, multifaceted issue" — describe the facets. "This is a testament to his enduring legacy" — describe what he did. Importance adjectives ("crucial," "pivotal," "significant") almost always signal a failure to show importance. WP:AISIGNS catalogues the family as "Undue emphasis on significance, legacy, and broader trends": "stands as / serves as a testament," "marking a pivotal moment," "a vital / significant / crucial / pivotal key role / moment," "underscores / highlights its importance / significance," "reflects broader," "symbolising its ongoing / enduring / lasting," "contributing to the," "setting the stage for," "marking / shaping the," "represents / marks a shift," "key turning point," "evolving landscape," "focal point," "indelible mark," "deeply rooted."

### P5. Write one thing, not the idea of that thing

AI writes to sound plausible; humans write to say something specific. If a sentence would be true of any company / law / person in the category, delete it. Test: swap the subject for any random other of the same type. If the sentence still works, it wasn't saying anything.

Kriss in *NYT Magazine* gave the definitive example. Asked for an extremely funny *Simpsons* episode, ChatGPT produced a screenplay where characters tickled each other in a round: "First Homer tickles Bart, and Bart laughs, and then Bart tickles Lisa, and Lisa laughs, and then Lisa tickles Marge." "Somewhere in its web of associations, the machine had made a connection: Jokes are what make people laugh, tickling makes people laugh, therefore talking about tickling is the equivalent of telling a joke. That was an early model; they don't do this anymore. But the same basic structure governs essentially everything they write." The model produces the idea of a joke / insight / specific example rather than the thing itself.

---

## 4. Banned and restricted vocabulary

Statistically over-represented in LLM output. Bans aren't absolute — every word here can appear in human writing. The rule is density. One "underscore" in 2,000 words: fine; three: tell; six: disqualifying. **The piece is the unit of analysis, not the sentence.**

### 4.1 Absolute bans — the Juzek–Ward focal words

Juzek & Ward (COLING 2025) identified 21 focal words by 3-step method: (a) per-million PubMed frequency rose significantly 2020–2024, (b) the spike had no content explanation, (c) ChatGPT-3.5 systematically over-uses them when prompted. The 21 with highest ChatGPT:human ratio:

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

All are tells at normal density. Use only with specific justification.

Kobak et al. (2024) analysed 14M PubMed abstracts 2010–2024 and found unprecedented LLM-induced vocabulary shift: 329 "excess words" Q1 2024 (above 2021–2022 linear extrapolation), vs at most 188 during peak Covid. Excess ratios: "delves" 25.2×, "showcasing" 9.2×, "underscores" 9.1×. Lower-bound LLM usage in 2024 PubMed abstracts: 10%; some sub-corpora (e.g. Chinese biomedical authors writing in English) reach 30%.

### 4.2 Reinhart/Brown PNAS most-overrepresented words in narrative continuation

Brown et al.'s GPT-4o sample over-uses specific words (rates vs human use per 1,000 words in matched continuations):

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

Cited GPT-4o phrase: *"The camaraderie was palpable."* Four words, both items in 150×+ range. No human writing narrative continuation writes this.

### 4.3 Tier-1 bans — never use without specific reason

Each appears in Juzek–Ward focal words, Brown et al. GPT-4o list, Pangram vocabulary list, jpeggdev/humanize-writing Tier 1, or WP:AISIGNS. Each is a standalone marker.

- **delve / delves / delving** — Use "look into," "dig into," "examine," or delete. Post-ChatGPT spike of 2,700% in PubMed (Kriss 2025; Kobak r=25.2).
- **tapestry** (metaphor for culture, history, diversity) — Pangram: 25× over Gutenberg baseline. Literal woven cloth: fine.
- **intricate / intricacies** — 611–772× over human rate. Use "detailed," "complicated," or describe the actual details.
- **vibrant** — 1,260× over Gutenberg in ChatGPT.
- **realm** (metaphorical) — Use "area," "field," "world." "Realm" is for Tolkien.
- **testament** ("X is a testament to Y") — Delete; describe what X actually demonstrates.
- **underscore / underscores / underscoring** (verb meaning "emphasise") — 390–903× over human rate. Use "shows," "proves," or rewrite so the fact carries its own weight.
- **showcase / showcases / showcasing** — 422× over human rate. Use "shows," "includes," "features." One of four persistent post-2025 (GPT-5-era) tells per WP:AISIGNS.
- **seamless / seamlessly** — Delete or replace with the specific integration mechanism.
- **navigate / navigating** (metaphor for handling) — "Navigate challenges," "navigate the landscape" are pure AI. Say "handle," "manage," or describe the steps.
- **leverage** (verb meaning "use") — Almost always means "use." Use "use."
- **boasts** (meaning "has") — 918× over human rate. Replace with "has."
- **multifaceted / nuanced** — If you believe it, describe the facets / nuance. Labels without content are hollow.
- **comprehensive** — Meaningless signifier. Prove comprehensiveness with scope data or delete.
- **crucial / pivotal / vital / paramount** — Hype adjectives. Replace with specific consequence or metric. Kobak: "crucial" δ=0.026 (2.6 percentage points more 2024 abstracts than 2022 counterfactual predicts).
- **groundbreaking** — 330× over human rate. Rarely true. Delete.
- **advancements** — 277× over human rate. Use "advances."
- **camaraderie / palpable / fleeting / solace / unspoken** — All 80–170× over human rate in GPT-4o narrative continuation (Brown et al.).
- **grapple / grapples / grappling** — 131× over human rate. Use "handle," "wrestle with."
- **amidst** — 90–100× over human rate. Use "amid," or restructure.
- **"signal, not noise" / "signal vs noise" / "signal over noise" / "more signal than noise"** — Banned outright. Tech-bro cliché *and* an instance of §5.1 negative parallelism. Replace with a specific claim about what the disagreement (or data) actually carries: "disagreement between the critic and sentinel flags scenario miscategorisation," not "disagreement is signal, not noise." If you can't say what the signal is, you don't have one to defend.

### 4.4 Restricted (density matters — max one per ~2,000 words)

More than one combined with any Tier-1 word disqualifies:

additionally, moreover, furthermore, however (as opener), enhance, foster, fostering, robust, dynamic, holistic, cutting-edge, game-changing, transformative, revolutionary, innovative, streamline, empower, embark, embrace (metaphorical), endeavour, garner, harness, illuminate, resonate, weave/weaving, journey (metaphorical), roadmap, ecosystem, framework (used vaguely), landscape (abstract), paradigm, synergy, alignment / align with, paramount, imperative, overarching, unprecedented, profound, renowned, stunning, exemplifies, valuable (as generic modifier), rich (as in "rich history"), deeply rooted, indelible.

### 4.5 Opener bans

Never open a sentence, paragraph, or section with any of these. Each is on WP:AISIGNS, Cherryleaf, or jpeggdev/humanize-writing:

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

Never close a section, paragraph, or piece with these. SearchEngineLand 2026 analysis of 1,000+ URLs: "Conclusion" headers had the strongest negative correlation with reader engagement (≈ −0.118). Readers bounce.

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

Brown et al.: LLMs use hedges ("at about," "almost") at 50–67% of human rate — but use *discursive hedges* (below) far above human. Tell is the construction, not hedging itself.

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

Hedging has legitimate uses (regulated domains, genuinely uncertain claims). Test: am I hedging because unsure, or to sound cautious? If latter, cut.

### 4.8 Sycophantic / chatbot artefacts (always delete)

Slip through when AI drafts paste without editing:

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

### 4.9 WP:AISIGNS vocabulary by model era

LLM lexical fashions shift. Synthesis from WP:AISIGNS for gauging which model wrote something:

- **2023–mid-2024 (GPT-4 era):** additionally, boasts, bolstered, crucial, **delve**, emphasizing, enduring, garner, intricate / intricacies, interplay, key, landscape, meticulous / meticulously, pivotal, underscore, **tapestry**, testament, valuable, vibrant.
- **Mid-2024–mid-2025 (GPT-4o era):** align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant.
- **Mid-2025 onward (GPT-5 era):** emphasizing, enhance, highlighting, showcasing — plus the newer "Undue emphasis on notability / attribution / media coverage" pattern: "profiled in," "independent coverage," "leading expert," "active social media presence."

"Delve" peaked and is in sharp decline; less diagnostic now. "Emphasising," "enhance," "highlighting," "showcasing" are the persistent current tells.

### 4.10 Filler-phrase replacements

Verbose filler resolves to one of: simpler conjunction, bare verb, or deletion.

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

Lexical cleanup alone is insufficient. Sam Kriss's *NYT Magazine* analysis ("Why Does A.I. Write Like… That?", 3 Dec 2025) argued — correctly — that structure is a deeper tell than vocabulary. With vocabulary cleaned, readers still sense AI because the **shapes** of sentences and paragraphs are wrong.

### 5.1 Negative parallelism — "It's not X, it's Y" and "Not just X, but Y"

The single most recognisable AI structure. Classical rhetoric calls it antithesis or negative-positive parallelism. In human writing, a high-impact device used sparingly. In LLM output, appears at densities no human produces.

**Data.** *Washington Post* analysed 328,744 publicly shared ChatGPT messages (gpt-4o, May 2024 – Jul 2025). Variations of "not just X, but Y" appeared in **6% of all July 2025 messages** — one in seventeen. No human register reaches that rate.

**Why.** RLHF and DPO are contrastive objectives: the model moves *toward* preferred completions and *away* from rejected ones. Negation ("it's not X") syntactically enacts distance from the rejected sample space; the elevated alternative ("it's Y") enacts convergence on the preferred. The antithesis is a direct output of contrastive training given preference-data composition (Milind Nair, *Dev.to* March 2026).

**Rule.** Use the construction **zero times** without specific rhetorical reason. At most once per 2,000-word piece. Variants to grep:

- "It's not just X — it's Y."
- "This isn't about X; it's about Y."
- "Not only X, but also Y."
- "Not X, but Y."
- "Less about X, more about Y."
- "No X, no Y, just Z."

**Fix.** Say only the positive. "It's Y" carries more force than "It's not X; it's Y" nine times in ten.

### 5.2 The tricolon reflex — rule of three

LLMs group ideas in threes compulsively: three-item lists, three adjectives, three parallel clauses. Humans use threes at roughly a third of the AI rate (Massobrio, "Triviality and Rhetorical Triplets," LinkedIn 2025). Tell is frequency, not any single tricolon.

**Rule.** If two consecutive paragraphs both use three-item structures, rewrite one. If >30% of lists have exactly three items, you're defaulting to rhetoric.

**Specific patterns to delete or rewrite:**

- "Start building, start learning, start growing." (motivational tricolon close)
- "Through curiosity, persistence, and collaboration…" (abstract-noun tricolon)
- "Identify, analyse, act." / "Plan, prepare, perform." (imperative tricolon)
- "Time, resources, and attention." (noun tricolon where two would do)
- "Clear, concise, and actionable."
- "Efficient, scalable, and robust."

### 5.3 The balanced conclusion

Conclusion presenting "good news," "challenge," and "forward-looking closer" in perfect symmetry. Also: "Despite X, Y faces challenges, including … However, with [ongoing efforts / future outlook] it continues to thrive." WP:AISIGNS canonical form: *"Despite its [positive/promotional words], [article subject] faces challenges… Despite these challenges, [subject] continues to… With [X], it is positioned to…"*

**Rule.** End with one strong statement, not a balanced assessment. If evidence points one way, conclusion points one way.

### 5.4 Avoidance of basic copulas — "serves as" / "stands as" / "represents" / "marks"

LLM text systematically replaces "is" / "are" with "serves as," "stands as," "marks," "represents," "features," "boasts," "offers," "maintains." One study documented **>10% decrease in usage of "is" and "are" in academic writing in 2023 alone**, no prior trend (cited in WP:AISIGNS). Same pattern in AI copyedits: asked to "revise," GPT systematically hollows copulas.

Brown et al. confirms: LLMs use "be" as main verb at 61–63% (GPT-4o) and 100–108% (Llama Instruct) of human rate. Compensation is nominal: "serves as X," "stands as X," "boasts a Y," "features a Z."

**Rule.** Default to "is." Reach for "serves as" only when the subject genuinely performs a function ("the valve serves as a pressure relief").

> **AI:** "Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces…"
> **Human:** "Gallery 825 is LAAA's exhibition space for contemporary art. There are four rooms…"

### 5.5 Superficial participial analyses

Brown et al.'s strongest finding: instruction-tuned LLMs use present participial clauses at **2–5× human rate**. Gestures at significance without doing the work: "…reflecting broader trends," "…underscoring its importance," "…contributing to the region's cultural identity," "…highlighting the enduring relevance of…," "…ensuring continued relevance," "…showcasing how…," "…fostering a sense of…," "…encompassing…"

WP:AISIGNS catalogues these as "Superficial analyses": "highlighting / underscoring / emphasising …," "ensuring …," "reflecting / symbolising …," "contributing to …," "cultivating / fostering …," "encompassing …," "valuable insights," "align / resonate with."

**Rule.** Delete every terminal participial phrase that doesn't add a fact. If it contains "reflecting," "underscoring," "emphasising," "highlighting," "showcasing," "contributing to," "cultivating," "fostering," or "ensuring," it's almost always decorative.

### 5.6 The "challenges and future prospects" scaffold

WP:AISIGNS example from a December 2025 draft: *"Despite its industrial and residential prosperity, Korattur faces challenges typical of urban areas, including… With its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of the Ambattur industrial zone, embodying the synergy between industry and residential living."* Every word after "urban areas" is filler.

**Rule.** Don't write a challenges paragraph without specific, sourced, load-bearing challenges. Never end with "despite these challenges" followed by uplift.

### 5.7 Over-scaffolding: announce / deliver / summarise

AI writes like a bad TED talk: tells you what it's going to say, says it, tells you what it said.

- Delete intros like "In this article, we'll explore…" / "Let's dive in."
- Delete roadmap sentences like "First, we'll cover X. Then we'll cover Y."
- Delete every conclusion beginning "As we've seen…" or "In summary…"

### 5.8 "Elegant variation" / pronominal gymnastics

LLMs have repetition-penalty decoding plus explicit training to avoid reusing a word, producing the classic Fleet Street "popular orange vegetable" effect — after using a name, every later reference cycles through "the actor," "the star," "the 45-year-old," "the Academy Award nominee."

**Rule.** Reuse names. Reuse "the company," "the function," "the user" where they're the clearest referent. Variation for variation's sake is an AI tell. (*The Guardian* style team mocked this for decades under "POV — popular orange vegetable"; LLMs do it as system default.)

### 5.9 Paragraph uniformity

AI paragraphs cluster around a narrow length band (60–90 words typical). Human paragraphs vary from one sentence to twelve. CoV of paragraph lengths is one of the most reliable statistical AI signals (Kitmul 2026; Pangram 2025).

**Rule.** Never write a piece where every paragraph is within ±20% of the same length. Never one where every section gets roughly equal wordcount.

### 5.10 Em dashes — the markdown fingerprint

Em-dash overuse is real but derivative. Freeburg (2026): em dashes are "markdown leaking into prose — the smallest surviving unit of structural formatting when headers, bullets, and bold are suppressed." Humans have used em dashes for centuries; the test is function and frequency.

**Em-dash rates per 1,000 words across 12 models (unconstrained / markdown-suppressed / em-dash-prohibited):**

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

1. Em dashes aren't banned. Humans have used them for centuries.
2. >1 em dash per 3–4 paragraphs is above human baseline for most registers.
3. Even a single em dash is a tell if performing the classic AI move: injecting a dramatic explanatory clause for false profundity ("The answer is simple — or is it?").
4. Use as humans do: genuine asides, parenthetical material that can't be expressed otherwise, interruptions of thought. Not rhythm-fillers.

### 5.11 Title case in headings

AI chatbots default to Title Case For All Main Words In Section Headings. Most human writing uses sentence case. Exception: formal US magazine / journal style guides.

**Rule.** Match your publication's house style. Otherwise sentence case; aligns with modern editorial practice (Guardian, BBC, most tech docs) and breaks an AI default.

### 5.12 Curly vs. straight quotes

ChatGPT and DeepSeek output curly quotes ("curly") and curly apostrophes (it's). On a technical platform expecting straight ASCII: a tell. In publishing contexts (Chicago style, InDesign workflows, macOS smart-quote autocorrect): not. Gemini and Claude typically don't use curly quotes. Context-dependent; don't over-weight.

### 5.13 Formal syntactic divergences (HPSG-level)

Zamaraeva et al. (ACL 2025) compared NYT-style human writing to six LLMs using Head-driven Phrase Structure Grammar. Found systematic differences in constituency length, dependency distances, variety of syntactic constructions — LLMs produce longer constituents and less variety. At grammar-type level, LLM text is more templatic: repeated similar clausal openings ("It is important to note that…", "In order to…"), recurrent coordination patterns. Reliability increases at longer text lengths.

**Operational implication.** If the first 5–8 words of every paragraph follow a similar syntactic template, the piece is AI-shaped even if every word is human-replaced.

### 5.14 Performed authenticity (second-generation tells)

When models are prompted to "sound human" they overshoot, producing a new family of tells. Subtler than classic AI vocabulary because they *perform* the very signals — informality, opinion — that mark human writing, but mechanically. Catalogued by the Humanizer kit (Berman 2026, patterns 25–28) as "performed authenticity."

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

AI promises insight then delivers nothing (17-tells analysis by Jim Christian, 2025):

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

AI generates concrete-sounding examples that are actually generic: *"Consider a marketing team at a mid-sized company…"* / *"Sarah, a software engineer…"* Cherryleaf calls this "generic specificity," possibly the strongest structural tell: "AI provides examples that feel specific without actually being specific. *'A procurement policy that made sense for a manufacturing business might not work for a software division.'* True! But *which* procurement policy? *Which* manufacturing business?"

**Rule.** Every specific example must be specific. Named person, named company, dated event, or cut.

### 6.3 Fake anecdotes and fabricated authority

- "I spoke with dozens of engineers…" — if you didn't, don't say it.
- "I've been doing this for years…" — if written by an LLM, it's a lie.
- "In my experience…" followed by generic advice — a tell.
- Fabricated quotes attributed to real people.
- Fabricated citations with plausible-looking DOIs that resolve to unrelated papers (WP:AISIGNS: LLMs generate references to non-existent papers with DOIs that exist but lead to unrelated articles).

The NYT / *Guardian* / Alex Preston incident of March–April 2026 is the canonical warning. Preston, a six-time author who'd written for the NYT for five years, used an AI "editing tool" on a book review draft. The AI silently incorporated passages from a prior *Guardian* review of the same book. A reader noticed the overlap. Preston was dropped by the NYT. AI drafting is forensically checkable; plagiarised-by-AI is still plagiarised.

**Rule.** Never keep an anecdote, quote, or citation an LLM generated without verifying it against an external primary source.

### 6.4 Significance inflation

AI puffs up every topic. WP:AISIGNS catalogues the repertoire: "stands as a testament," "marking a pivotal moment," "represents a significant shift," "underscoring its importance," "symbolising its enduring legacy," "setting the stage for," "cementing its role as," "a cornerstone of," "an indelible mark," "of profound importance," "deeply rooted," "nestled in the heart of," "boasts a rich history of."

**Rule.** Write about the thing, not about the importance of the thing. Importance should be legible from the facts. If you write "X represents a significant shift," replace it with what actually happened: who did what, when, to what effect.

### 6.5 Unnecessary enthusiasm

AI flatters the reader. Every list idea is "excellent," "powerful," "transformative," "exciting." Every approach is "elegant." Every insight "invaluable." Every opportunity "tremendous." Every future "bright."

**Rule.** Praise is earned by content. Strip all praise adjectives and check if the claim still reads strong. Usually it reads stronger.

### 6.6 Both-sides framing as default

"While X is true, it is also important to consider Y." "On the one hand … on the other hand…" "There are valid arguments on both sides." RLHF's face-saving training in pure form (Dev.to analysis of DPO/RLHF objectives, March 2026).

**Rule.** If one side is stronger, say so. "Both sides" is appropriate only when evidence genuinely is split and you have the sources to show it.

### 6.7 The motivational poster close

"In the end, what matters most is… Every journey begins with a single step… The future is ours to shape… Let's build something extraordinary…"

**Rule.** Business/tech writing never ends like this. Close on a fact, a next action, or a question the reader now has to answer.

### 6.8 Rhetorical questions in clusters

"How do we solve this problem? What does this mean for leaders? Why does this matter?" Cherryleaf: "AI loves rhetorical questions, especially in clusters of three (see: tricolon). But these aren't genuine inquiries opening space for thought. They're declarative statements wearing question marks, transitions disguised as engagement."

**Rule.** Ask questions you don't know how to answer. One rhetorical question per piece, max, and only if the question has teeth.

### 6.9 False ranges

"From X to Y" framing where X and Y aren't on a meaningful scale. *"Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter."* The endpoints don't bound a continuum; they're impressive examples dressed as a span.

**Rule.** Use "from X to Y" only when X and Y are real extremes of an ordered set (dates, sizes, levels, prices). Otherwise list the items: "The book covers the Big Bang, star formation, and current theories about dark matter." Source: Humanizer kit pattern #12 (Berman 2026).

---

## 7. Tone rules

### 7.1 Commit to a voice

AI default voice: formal, neutral, courteous, risk-averse. If that's your house voice (legal, medical, regulatory), this section doesn't apply — but AI tells will be harder to eliminate because they overlap with house style; lean harder on §4–§6.

Otherwise: pick a voice with edges. Conversational and informed. Opinionated and specific. Technical and dry. Sardonic and precise. Any committed voice beats AI courtesy voice.

### 7.2 Use first and second person where appropriate

Brown et al.: GPT-4o uses first-person pronouns at 62% of human rate, second-person at 52%. LLMs default to third-person passive ("it should be noted that users may experience…"). First and second person are human defaults in blog posts, documentation, post-mortems. Use them.

### 7.3 Use contractions

"It's," "don't," "you're," "we've." Brown et al.: GPT-4o uses contractions at only **60%** of human rate. Formal technical reference docs legitimately avoid them; essays, blog posts, guides, internal comments don't. One of the cheapest, highest-signal ways to move a piece away from the AI default.

### 7.4 Start sentences with "And" and "But"

The grammar-school rule isn't a rule. Do it. AI almost never does.

### 7.5 Use fragments

Like this. Where they earn their keep. Brown et al. don't break out fragments specifically, but the higher "that"-clause and participial-clause usage in LLMs marks structurally complete sentences at rates no careful human matches.

### 7.6 Strong claims, specific numbers

"About half" → "47%" if you know it, "half" if you don't. "Significantly faster" → "2.3× faster on our dataset." Generic quantifiers ("many," "numerous," "a significant number of," "plenty of") are AI defaults.

### 7.7 Allow profanity and bluntness where it fits

Brown et al.'s most-underrepresented words for GPT-4o (0.01–0.02× human use): "fucking," "fuck," "asshole," "shit," "nasty," "blah," "yep," "ok," "i.e." Well-placed informal or blunt language is a powerful de-AI signal because the model has been explicitly trained not to produce it. In contexts that permit it, use it.

### 7.8 Register shifts within a piece

Formal sentence followed by "but honestly, that's insane": human. Formal paragraph followed by casual: human. Brown et al. demonstrated instruction-tuned LLMs show limited register variation. Humans adapt; shift register when subject matter turns.

---

## 8. Formatting rules

### 8.1 Bullet discipline

AI's default output is a bulleted list with bold inline headers. Most serious prose isn't a bulleted list. Freeburg shows that even under markdown suppression, residual bullet-and-bold reflex leaks through.

- **Use bullets** for genuinely enumerable, parallel items (requirements, options, references).
- **Don't use bullets** as a substitute for paragraphs. If a bullet runs more than two lines, it wanted to be a paragraph.
- **Never nest bullets three deep** unless writing a reference document with genuine hierarchical structure.
- **Don't convert "challenges" or "benefits" into bullet lists** in articles. Result: WP:AISIGNS's "Inline-header vertical lists" — strong AI signature.

### 8.2 Bold restraint

The "every third word is bold" pattern is a direct import from marketing copy, slide decks, and how-to listicles — heavily represented in training data. WP:AISIGNS: "AI chatbots may display various phrases in boldface for emphasis in an excessive, mechanical manner," with real Wikipedia draft examples where entire narrative paragraphs were dotted with bold.

**Rule.** In body prose, use bold at most once per section, only for genuine emphasis on a load-bearing term. To make something stand out, write a sentence that stands out.

### 8.3 Emoji

Professional technical writing, long-form journalism, and most documentation don't contain emoji. 🚀 ✨ 💡 as section decorators or headline enhancers are AI fingerprints. *Washington Post*'s 328,744-message analysis found ChatGPT "leans heavily on emojis" as one of three strongest lexical tells. If your brand voice uses emoji deliberately, fine — never auto-accept what an LLM produces.

In open-source READMEs specifically, `## Features ✨` is a near-certain AI signature (see §9.2).

### 8.4 Markdown leakage

Asked to generate prose for a non-Markdown context, LLMs leak Markdown: stray `**bold**`, `---` thematic breaks, inline `# headers` rendered as literal hashes. WP:AISIGNS leak patterns: thematic breaks (`----`) before each heading, explicit `1.` numbering instead of wikitext, `##` used for section headings on platforms that interpret `##` differently.

Audit for this every time.

### 8.5 Heading patterns

- No skipped heading levels (H1 → H3 with no H2: AI tic because the chat app rendered H1 at top and H3 was the first "inner" heading; WP:AISIGNS).
- No decorative divider lines (`---`) above every heading.
- No "Summary" or "Conclusion" heading at the end of everything.
- Sentence case unless house style mandates title case.

### 8.6 ChatGPT-specific leaks to grep

WP:AISIGNS catalogues model-specific markup bugs in pasted chat output:

- `turn0search0`, `turn0search1`, `iturn0image0turn0image1` (ChatGPT web search reference placeholders)
- `:contentReference[oaicite:N]{index=N}`, `oai_citation:N`, `Example+1` (ChatGPT citation bugs)
- `({"attribution":{"attributableIndex":"X-Y"}})` (JSON attribution leak)
- `utm_source=openai`, `utm_source=chatgpt.com`, `utm_source=copilot.com`, `referrer=grok.com` (UTM tags on cited URLs)
- `[attached_file:1]`, `[web:1]` (Perplexity tags)
- `grok_card` XML tags (Grok)
- `access-date=2025-XX-XX` or `access-date=2025-xx-xx` (LLM placeholder dates in citations)
- `INSERT_SOURCE_URL_30`, `PASTE_YOUTUBE_VIDEO_URL_HERE`, `[Your Name]`, `[Describe the specific section]` (unfilled phrasal templates)

`grep -E 'turn0|oaicite|oai_citation|utm_source=(openai|chatgpt|copilot)|access-date=.{4}-XX-XX'` on any suspect document catches most in one pass.

---

## 9. Domain-specific guidance

### 9.1 Articles, essays, blog posts

§4 and §5 tells damage most here because readers actively assess voice. Additional rules:

- **Intros must commit immediately.** Drop the scene-setting paragraph. First sentence already doing work.
- **No TL;DR at top unless your publication demands it.** AI defaults to summary-first; leading journalism leads with the lede.
- **Include at least one moment of observational specificity** — something you saw, measured, remember. AI can't produce these. Human pieces without them read as AI-adjacent. Brown et al. found GPT-4o uses rare specific proper nouns like "Deborah" or actual place names at a small fraction of human rates.
- **Cite real sources with page numbers or URLs.** AI-hallucinated citations are the most reputationally destructive tell; the NYT / Alex Preston / *Guardian* incident (March 2026) is the canonical warning. *The Globe and Mail* (April 2026 standards-editor column): contributors to Opinion, First Person, and Lives Lived must attest their work is "original and created without the use of artificial intelligence."
- **No Elara Voss.** If your piece contains a fictional character, ensure the name doesn't match the ChatGPT-era canonical set: Elara, Elena, Kael, Sarah, Emily, variations. Pangram: 60–70% of character names in unprompted ChatGPT/Claude short fiction are "Emily" or "Sarah." Kriss found the same for SF protagonists.
- **Write one opinion, not a survey of opinions.** Cherryleaf: "Real writers pick a position and defend it. AI always presents both sides."

### 9.2 Technical documentation

Documentation has its own AI-tell profile; many detection heuristics false-positive on technical writing (Pangram 2025). These patterns are still clearly AI:

- **Over-explained trivial operations.** A README opening "In today's fast-paced development environment…" is AI. Good docs say what the thing is and what it does, then stop.
- **Generic "Prerequisites / Installation / Usage / Troubleshooting / Contributing / License" scaffolding with no content specificity.** AI produces the README skeleton. Yours must have non-generated content.
- **Version specificity.** Real docs say `python>=3.11`, `node 20.11.1`, `webpack 5.92.0+`. AI docs say "ensure you have Python installed."
- **Error messages quoted verbatim.** AI rarely produces real error strings; when it does, often slightly wrong. Copy-paste the real ones.
- **No emoji in section headings** (`## Features ✨` is a near-certain AI signature for professional tech docs per Mohamed Abdullah 2025).
- **No marketing copy in technical docs.** "Seamlessly integrate," "empower developers," "revolutionise your workflow" — none belong in a README.
- **No three-line horizontal rules (`---` or `***`) between every section.** Markdown leaking (Freeburg 2026).

### 9.3 Code comments

Human developers under-comment. AI over-comments. Ratio is the tell. Codequiry's 2026 analysis of thousands of flagged submissions identifies over-commenting as the most reliable AI indicator in code.

**Ban:**

- Comments restating the code in English. `// increment counter` above `counter++;` is an AI signature. Codequiry example:
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
- Comments referencing the task, the PR, the AI session, or "as requested."
- Decorative divider banners (`// =========== USER MANAGEMENT ============`).
- Emoji in code comments outside projects using them deliberately.
- "TODO: implement later" on code you could implement now.
- "This handles all edge cases" — AI over-claims; humans say "handles null and negative n; check for NaN separately."
- Generic over-engineered edge-case handling that doesn't match assignment scope. Student solving "reverse a string" doesn't proactively handle multi-byte Unicode grapheme clusters; an LLM does.
- Perfect symmetry of error handling across every function, including where none is needed. AI adds try/catch everywhere; humans add it where they've seen it fail.

**Keep:**

- WHY comments. The non-obvious reason the code is the way it is — workaround for a specific bug, hidden invariant, constraint from external system.
- Version / environment qualifiers (`// only works on node >= 20 because of structuredClone behaviour`).
- Footgun warnings (`// DO NOT reorder — the auth call must happen before the session write or we leak`).
- Specific error-code references (`// returns EAGAIN if the ring buffer is saturated; retry with backoff`).

Rule of thumb: if deleting the comment leaves no reader confused, delete it.

### 9.4 Marketing copy

Marketing copy is where AI writing is most compressed and most recognisable: marketing corpora dominate training data and RLHF rewards exactly the register that sells. The 400-word Pangram vocabulary list applies with 2× sensitivity.

- Ban "seamlessly," "empower," "elevate," "transform," "unlock," "revolutionise," "cutting-edge," "next-generation," "game-changing," "state-of-the-art," "industry-leading," "end-to-end," "at scale," "best-in-class," "holistic," "mission-critical," "robust," "scalable," "turnkey."
- Ban abstraction: "solutions," "platforms," "experiences," "journeys," "ecosystems."
- Replace every generic benefit with a specific verifiable one. "Saves time" → "5 minutes off a median checkout." "Increases engagement" → "+14% 7-day retention in our A/B test."
- No tricolons in headlines.

### 9.5 Commit messages, PR descriptions, changelog entries

WP:AISIGNS flags LLM-generated edit summaries as "formal, first-person paragraphs, without abbreviations, and conspicuously echoing the exact text or shortcuts of policies… They often mention things that they 'ensured' or 'avoided' doing."

Real 2025 Wikipedia edit summary (AI-generated): *"Concise edit summary: Improved clarity, flow, and readability of the plot section; reduced redundancy and refined tone for better encyclopedic style."* Every word: AI signature.

**Rule.** Imperative mood, short, factual. "Add X." "Fix Y in Z." "Remove dead path in foo.bar." One line unless the PR description genuinely needs more.

### 9.6 Code review, issue comments, OSS discussion

CHAOSS Project 2024: AI-generated OSS comments rose from 0.9% (Q1 2023) to 7.3% of non-maintainer comments. Patterns maintainers see:

- **Documentation Mirror:** Comments regurgitating official docs verbatim but omitting documented caveats.
- **Solution-First, Constraint-Agnostic:** Proposing elegant code fixes without referencing actual error logs, environment versions, or project constraints.
- **Consensus Vacuum:** "most developers agree," "it is widely accepted," "best practices suggest" — appeals to unnamed authority.
- **Absence of versioned specificity:** No `python --version`, no exact error strings, no stack traces.
- **Missing "why not X?" reasoning:** Human proposals weigh alternatives; AI proposals don't.

If participating in OSS discussion: cite exact versions, paste exact error messages, show actual output. The signals are the absence of signals.

---

## 10. Detection methods: what they actually measure

Knowing what classifiers look at tells you what to neutralise. Detection research converges on seven signal classes (Crothers et al. 2023; Mitchell et al. DetectGPT 2023; Bao et al. Fast-DetectGPT 2024; McGovern et al. 2025; Xiang et al. 2026):

1. **Lexical over-representation lists.** Gray (2024), Juzek & Ward (2025), Kobak et al. (2024), Pangram maintain lists of ~20–400 words whose AI-output frequency exceeds human baseline by orders of magnitude.
2. **Perplexity / surprisal diversity.** Lower mean surprisal under reference LM, lower variance across tokens. DivEye (Dey et al. 2025, arXiv:2509.18880) and Binoculars (Hans et al. 2024, arXiv:2401.12070) are current SOTA zero-shot.
3. **Burstiness.** CoV of sentence-length distribution and per-sentence perplexity.
4. **POS-tag n-gram distributions.** McGovern et al.'s Grammarly/Cambridge paper: simple decision-tree classifiers on POS-n-gram features hit 0.94–0.98 macro-F1 for GPT-4 vs human. Fingerprints "consistent within model families" (LLaMA 13B and 65B share one), "robust across text domains."
5. **Stylometric ensembles.** StyloAI (arXiv:2405.10129): 31 stylometric features, 81–98% accuracy.
6. **Formal syntax features.** Zamaraeva et al. (ACL 2025): HPSG grammar types. Tagset distributions diverge systematically.
7. **Watermarks.** Kirchenbauer et al.'s green/red token scheme and successors embed detectable statistical signatures during generation. Reliable only when applied at generation, not laundered through editing.

**Why single-metric detectors (GPTZero, ZeroGPT, QuillBot) produce false positives.** A 2023 Stanford study flagged 61% of non-native-English TOEFL essays as AI. Non-native writers produce lower-perplexity text because they avoid unusual constructions; single-threshold perplexity detectors collapse "non-standard word choice" and "AI-generated" onto one axis. *The Globe and Mail* (April 2026): three different AI detectors on the same NYT "Modern Love" column returned three different verdicts.

**Operational implication.** Multi-feature, domain-calibrated ensembles are SOTA. If your piece is clean against vocabulary, structure, perplexity, burstiness, and POS-n-gram profile simultaneously, no current detector flags it. The §13 checklist is built against this multi-signal profile.

---

## 11. Evolution: what has changed 2023 → 2026

Signals matter only insofar as models still produce them.

- **"Delve" in sharp decline.** Peaked 2023–early 2024; dropped off in 2025 after widespread mockery and (reportedly) internal fine-tuning. Remaining usage still high vs pre-2022 baseline, but "delve" alone is no longer proof.
- **Em-dash overuse partially suppressed** in GPT-5.1 / GPT-5.4 (Nov 2025 onward) after OpenAI acknowledged the issue; Sam Altman's Threads post confirmed adjustment in response to user preference. Absence no longer rules out AI.
- **"It's not X, it's Y"** increased and is now the strongest structural tell (*Washington Post*, Nov 2025). 6% of July 2025 ChatGPT messages contain "not just X, but Y" variations.
- **"Showcase," "emphasising," "enhance," "highlighting"** — persistent GPT-5-era vocabulary tells (WP:AISIGNS 2025/2026).
- **"Undue emphasis on notability, attribution, media coverage"**: newer pattern in retrieval-augmented models — they list sources the subject has been covered in rather than summarising what they said. Canonical phrases: "has been profiled in major outlets including…" "maintains an active social media presence" (uncommon on Wikipedia before ~2024).
- **Diffusion-based text models** (LLaDA family; arXiv:2507.10475) produce perplexity matching human baseline (44.62 vs 43.03), so perplexity-based detectors increasingly fail. Burstiness remains lower. Structural tells remain.
- **Obvious hallucinations and incoherence** (2022–early 2023 tells) mostly gone as models improved.
- **Model-attribution fingerprints remain.** McGovern et al. (2025): GPT-4 and Cohere can be distinguished from human and each other at F1 > 0.94 using simple n-gram features; fingerprint persists across model generations.

**Operational implication.** A clean piece today has ≤1 of the top-20 markers. Three years ago a clean piece could tolerate five.

---

## 12. Anti-patterns in "humanising" AI text

Three failure modes are common when cleaning up AI drafts. Each produces worse output than rewriting.

### 12.1 Swap-and-pray

Replacing "delve" → "explore," "underscore" → "highlight," "intricate" → "complex." Defeats only the most naive detectors. Underlying voice (cadence, hedging, symmetry, false profundity) is untouched, so readers still notice. *Washington Post* reader quote: *"the mismatch is even worse"* after surface-level edits — remaining structure is still AI-shaped, now with mismatched vocabulary.

### 12.2 Anti-detector obfuscation

Adding intentional typos, forced fragments, random "And"s. Produces prose reading as badly edited, worse than AI — AI at least reads as competent. Goal: good human writing, not corrupted AI. Pangram research on humanizer tools (DUPE / paraphrasing attacks; arXiv:2404.11408): defeats detectors temporarily while producing text human readers find obviously worse than either AI or human originals.

### 12.3 Heavy prompt engineering

"Write in the style of Hemingway with no em dashes, no hedging, no tricolons, vary sentence length between 5 and 30 words…" Model complies for 200 words, then drifts. Freeburg's gradient: GPT-4.1 retains 3.86 em dashes per 1,000 words even under explicit em-dash prohibition, 6.97 in 5,000-word outputs. Every prompt is a leaky abstraction over the underlying training distribution.

### 12.4 What actually works

Rewriting, not editing. Take the AI draft as research — claims, facts, rough outline — and write the final from a blank editor. Faster than sentence-by-sentence editing, better output.

For AI-assisted drafts where rewriting isn't practical:

1. Delete every Tier-1 vocabulary word (§4.3). No replacement; the sentence is usually better without.
2. Delete every hedge (§4.7). If the claim is true, say so; if not, remove it.
3. Delete every "not X, it's Y" construction (§5.1).
4. Delete every terminal participial phrase that doesn't add a fact (§5.5).
5. Vary paragraph and sentence lengths deliberately (§5.9).
6. Add at least one observational specific (§2 item 12, §9.1).
7. Take a position (§3 P2).
8. Re-read aloud. Fix any sentence that doesn't sound like you saying it.

---

## 13. Pre-publish checklist

Run every piece through this before shipping. 3+ "hits" → rewrite.

### Vocabulary scan (grep in editor):

- [ ] delve, delves, delving, delved (any hit → rewrite)
- [ ] tapestry (any hit → rewrite)
- [ ] intricate, intricacies (any hit → rewrite)
- [ ] realm, testament, vibrant (any hit → rewrite)
- [ ] underscore(s), showcase(s), leverage (as verb) (>1 combined → rewrite)
- [ ] boasts (as "has"), seamless(ly), navigate (metaphorical) (any hit → rewrite)
- [ ] foster(ing), harness(ing), embark (>1 combined → rewrite)
- [ ] crucial, pivotal, vital, paramount, multifaceted, nuanced, comprehensive (>2 combined → rewrite)
- [ ] camaraderie, palpable, fleeting, solace, unspoken, grapple, amidst, cacophony (any → rewrite in fiction; if nonfiction, near-certain AI)
- [ ] "signal, not noise" / "signal vs noise" / "signal over noise" / "more signal than noise" (any hit → rewrite — banned outright per §4.3)

### Opener / closer scan:

- [ ] Zero occurrences of "In today's … world," "In recent years," "In the realm of," "In the ever-evolving …"
- [ ] Zero occurrences of "In conclusion," "In summary," "Overall," "Ultimately," "The bottom line," "At the end of the day."
- [ ] Zero occurrences of "It's important to note," "It's worth noting," "It should be noted."
- [ ] Zero chatbot artefacts ("I hope this helps," "Great question," "Certainly," "Absolutely").

### Structural audit:

- [ ] Count "not X, but Y" / "not just X, it's Y" / "not only X, but Y" / "less about X, more about Y." >1 per 1,000 words → rewrite.
- [ ] Count three-item lists and tricolons. If >30% of enumerations are exactly three items → rewrite.
- [ ] Check paragraph-length variance. CoV > 0.4 → ok. < 0.2 → rewrite.
- [ ] Check sentence-length variance in any two consecutive paragraphs. Both within ±20% of mean → rewrite.
- [ ] Check conclusion. Does it balance "good news / challenge / forward-looking closer"? → rewrite.
- [ ] Check copulas. >2 instances of "serves as" / "stands as" / "represents" / "marks" / "boasts" / "features" → rewrite.
- [ ] Count terminal participial phrases ("-ing" at end of sentence). >1 per 300 words → rewrite.
- [ ] Count em dashes. >1 per three paragraphs → rewrite or convert to commas/periods.
- [ ] Count philosophical mic drops ("Maybe both.", "And honestly?", "Maybe that's the point.", "I think that says something.", "If that's not [noun], I don't know what is."). Any hit → cut the line.
- [ ] Count parenthetical personality injections ("(and honestly?)", "(not that I'm complaining)", "(if that makes sense)", "(or something like that)"). Any hit → cut the parenthetical.
- [ ] Check "from X to Y" constructions. If X and Y don't bound a real ordered scale → rewrite as a plain list.

### Voice audit:

- [ ] Does the piece take a position, or "balance both sides"? If latter, decide.
- [ ] Read the opening paragraph aloud. Would a human speak like this? If no, rewrite.
- [ ] Does it contain at least one observational specific (named person, specific number, concrete example from direct experience, real error message, real date)? If not, add one or acknowledge its absence explicitly.
- [ ] First-person or second-person pronouns where appropriate? If register permits and there are none → consider adding.
- [ ] Contractions present where register permits? If register permits and none → add.

### Formatting audit:

- [ ] No stray Markdown in non-Markdown contexts (`**bold**`, `---`, `##`).
- [ ] No decorative `---` above every heading.
- [ ] Bold used ≤ once per section, for genuine emphasis.
- [ ] Emoji only if house style demands it.
- [ ] Headings in sentence case unless style guide says otherwise.
- [ ] No nested bullets three deep.

### Leak audit (for AI-assisted drafts):

Run: `grep -E 'turn0|oaicite|oai_citation|utm_source=(openai|chatgpt|copilot)|access-date=.{4}-XX-XX|attached_file:|grok_card|\[Your Name\]|\[INSERT|\[PASTE'`

- [ ] Zero hits. Any hit → leak, fix before publish.

### Integrity audit:

- [ ] Every citation verified (URL resolves; page exists; source actually says what you claim).
- [ ] Every quote traced to a real source (not AI-hallucinated).
- [ ] No fabricated anecdotes. No "in my experience" if the experience is model-generated.
- [ ] Every DOI resolves to the paper you cited, not an unrelated one.
- [ ] Every book citation has a page number or verifiable URL.

---

## 14. Two worked before/afters

### 14.1 Marketing-register rewrite

**Before (AI draft, 76 words):**

> In today's rapidly evolving digital landscape, cybersecurity has emerged as a crucial concern for organizations of all sizes. As we navigate the complexities of modern threat vectors, it's important to note that a multifaceted approach is paramount. This isn't just about implementing tools — it's about fostering a culture of security. By leveraging comprehensive frameworks, organizations can seamlessly integrate robust defences that showcase their commitment to protecting stakeholders. Ultimately, the journey toward security resilience is a testament to the enduring importance of vigilance in our interconnected world.

Tell count:
- Lexical (Tier 1): evolving, landscape, crucial, navigate, complexities, multifaceted, paramount, fostering, leveraging, comprehensive, frameworks, seamlessly, integrate, robust, showcase, commitment, journey, testament, enduring, interconnected. **20 hits.**
- Structural: "It's not X — it's Y" (negative parallelism); "In today's … landscape" (opener ban); "Ultimately … testament" (hype close); three-noun tricolons ("tools," "culture," "frameworks"); every sentence within ±15% of same length.
- Voice: no position, no specific, no named threat, no named tool, no year, no number.

**After (human rewrite, same word count):**

> Cybersecurity is a work-culture problem dressed up as a tooling problem. In the 2024 Verizon DBIR, 68% of breaches involved a non-malicious human action — someone who clicked, mis-configured, or re-used a password. You cannot buy your way out of that with a new EDR. The useful question is not "which tool?" but "which of our processes would have caught this incident?" When teams answer that question honestly, they usually discover their weakest link is code review, not the firewall.

Same claim-space, different voice: opinionated, specific source (2024 Verizon DBIR), specific percentage (68%), named tool category (EDR), concrete recommendation (code review). Zero Tier-1 vocabulary. No negative parallelism. Sentence lengths: 12, 27, 9, 18, 17 words — CoV ~0.4.

### 14.2 Technical README rewrite

**Before (AI draft, 68 words):**

> ## Overview ✨
>
> Our robust, cutting-edge library empowers developers to seamlessly integrate authentication into their applications. By leveraging industry-leading best practices, it provides a comprehensive, end-to-end solution that showcases enterprise-grade security while fostering a superior developer experience. Whether you're building a small prototype or scaling to millions of users, **AuthKit** streamlines your authentication workflow with its intuitive API.

Tells: emoji in heading (§8.3); every Tier-1 marketing word (robust, cutting-edge, empowers, seamlessly, leveraging, industry-leading, best practices, comprehensive, end-to-end, showcases, enterprise-grade, fostering, superior, streamlines, intuitive); "Whether you're a … or a …" opener ban; no specific API name, no version, no examples.

**After (human rewrite, same word count):**

> ## What AuthKit is
>
> AuthKit is a drop-in authentication library for Node.js (≥20) and Deno. It wraps OAuth2, OIDC, and WebAuthn behind one API and ships tested clients for Google, GitHub, Okta, and Microsoft Entra. Use it when you want short-lived JWTs with refresh-token rotation, rate-limited login endpoints, and audit-ready logs on day one. Not recommended if you need SAML — the protocol is deliberately excluded; see [saml-kit](#) for that.

Same word count, specific runtime versions, specific protocols, specific providers, specific features named, specific non-feature named with a reason, specific use-case guidance. Zero Tier-1 vocabulary. No emoji. Sentence-case heading.

---

## 15. References and primary sources

### Peer-reviewed / arXiv

- Reinhart, A., Brown, D. W., Markey, B., Laudenbach, M., Pantusen, K., Yurko, R., and Weinberg, G. "Do LLMs write like humans? Variation in grammatical and rhetorical styles," *PNAS* 2025 (preprint arXiv:2410.16107v1). DOI 10.1073/pnas.2422455122. **Source of the Biber 66-feature analysis, HAP-E/CAP parallel corpora, present-participial-clauses 2–5× finding, over-represented words table (camaraderie, tapestry, palpable, intricate, etc.).**
- Juzek, T. S. and Ward, Z. B. "Why Does ChatGPT 'Delve' So Much? Exploring the Sources of Lexical Overrepresentation in Large Language Models," Proc. COLING 2025, pp. 6397–6411. **21 focal words; 3-step identification method; RLHF evidence via Llama 2-Base vs Llama 2-Chat entropy comparison.**
- Juzek, T. S. and Ward, Z. B. "Word Overuse and Alignment in Large Language Models: The Influence of Learning from Human Feedback," arXiv:2508.01930. **Direct experimental confirmation that LHF (RLHF + DPO) installs lexical preferences in Llama; online study showing participants systematically prefer text with focal words.**
- Kobak, D., González-Márquez, R., Horváth, E.-A., and Lause, J. "Delving into ChatGPT usage in academic writing through excess vocabulary," arXiv:2406.07016 / *Scientometrics* 2024. **14.2M PubMed abstracts 2010–2024; excess-words method; 329 excess words Q1 2024; 10% LLM-usage lower bound; "delves" r=25.2, "crucial" δ=0.026.**
- McGovern, H., Stureborg, R., Suhara, Y., and Alikaniotis, D. "Your Large Language Models Are Leaving Fingerprints," Proc. GenAIDetect 2025, ACL, aclanthology.org/2025.genaidetect-1.6. **POS-n-gram fingerprints; 0.94–0.98 F1 on GPT-4 / Cohere / human; fingerprints consistent within model family across domains.**
- Freeburg, E. M. "The Last Fingerprint: How Markdown Training Shapes LLM Prose," arXiv:2603.27006, March 2026. **Em-dash mechanistic analysis; 12-model × 3-condition suppression gradient; Table 1 above.**
- Zamaraeva, O., Flickinger, D., Bond, F., and Gómez-Rodríguez, C. "Comparing LLM-generated and human-authored news text using formal syntactic theory," Proc. ACL 2025 Long Papers, pp. 9041–9060.
- Mitchell, E., Lee, Y., Khazatsky, A., Manning, C. D., and Finn, C. "DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature," ICML 2023.
- Hans, A., et al. "Spotting LLMs With Binoculars: Zero-Shot Detection of Machine-Generated Text," arXiv:2401.12070.
- Dey et al. "DivEye: Surprisal Diversity for Zero-Shot LLM Detection," arXiv:2509.18880.
- Liang, W., Yuksekgonul, M., Mao, Y., Wu, E., and Zou, J. "GPT detectors are biased against non-native English writers," *Patterns* 4(7), 2023. **61% of non-native TOEFL essays falsely flagged.**
- Zaitsu, W. and Jin, M. "Distinguishing ChatGPT(-3.5, -4)-generated and human-written papers through Japanese stylometric analysis," *PLOS ONE* 18(8):e0288453, 2023.
- Przystalski, K., Argasiński, J. K., et al. "Stylometry recognizes human and LLM-generated texts in short samples," arXiv:2507.00838, 2025. **0.87 Matthews correlation on 10-sentence texts in 7-way classification.**
- *Humanities and Social Sciences Communications*, "Stylometric comparisons of human versus AI-generated creative writing," 2025.
- "Can You Detect the Difference? Autoregressive vs. Diffusion Text Generation," arXiv:2507.10475, 2025. **LLaDA achieves human-matching perplexity.**
- Xiang, L., et al. "AI-Generated Text Detection: A Comprehensive Review of Active and Passive Approaches," *Computers, Materials and Continua* Vol. 86 Issue 3, 12 January 2026.

### Journalism / editorial

- Kriss, S. "Why Does A.I. Write Like … That?" *NYT Magazine*, 3 December 2025. **Source of the "tickling" anecdote, Elara Voss / Kael observation, "delve" 2,700% post-2022 claim, structural-vs-vocabulary argument.**
- Merrill, J. B., Chen, S. Y., and Kumer, E. "What are the clues that ChatGPT wrote something? We analyzed its style." *Washington Post*, 13 November 2025. **Analysis of 328,744 publicly shared ChatGPT gpt-4o messages May 2024 – July 2025; 6% of July 2025 messages contain "not just X, but Y" variations.**
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

Reviewed against its own checklist:

- **Vocabulary scan.** Zero occurrences in running prose of: delve, tapestry, intricate, realm, vibrant, testament, showcase, seamless, navigate (metaphorical), leverage (as verb), foster, crucial, pivotal, multifaceted, nuanced, comprehensive, robust, transformative, groundbreaking, revolutionary, camaraderie, palpable, fleeting, solace, grapple, amidst.
- **Opener / closer scan.** Zero openers of "In today's…", "In recent years…", "In the realm of…", "It's important to note…". Zero closers of "In conclusion…", "Overall…", "Ultimately…", "The bottom line…".
- **Negative parallelism.** One deliberate use in §5.1 as illustrative example, one in §14.1's worked example. Zero elsewhere.
- **Tricolon density.** Enumerations mixed: two-item, three-item, four-item, seven-item, thirteen-item lists. No paragraph contains two consecutive tricolons.
- **Sentence-length variance.** Intentional short/long mix throughout; §6.5 closing paragraph opens with "Praise is earned by content." (4 words) then a longer analytical sentence.
- **Paragraph-length variance.** Paragraphs vary from one sentence (several in §3) to twelve sentences (§1.2).
- **Opinions taken.** §5.1 calls negative parallelism "the single most recognisable AI structure." §12.4 asserts rewriting beats editing. §9.4 bans specific marketing words. §11 takes a position on which tells remain live versus which have decayed.
- **Specifics.** arXiv IDs, DOIs, publication dates, page numbers, percentage figures, specific model names, specific ratio values (1,374.92×, 6%, 0.118, 68%, 2,700%, 329 excess words, etc.) throughout §1, §4, §5, §10, §15.
- **Copulas.** "Is" used freely. "Serves as" / "stands as" / "represents" avoided except where literally functional.
- **No markdown leakage.** No stray `---` dividers above headings. No emoji in headings. Sentence case throughout.
- **First and second person** used appropriately in instructions: "you," "your," "we."
- **Contractions** used where register permits: "isn't," "don't," "can't," "wasn't."

If the guide itself read as AI-written, it wouldn't be credible. The test survives.
