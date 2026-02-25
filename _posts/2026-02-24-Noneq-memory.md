---
title: '日記：大雪とSpecial Chez Pierre'
date: 2026-2-24
permalink: /posts/2026/2/Noneq-memory/
tags:
  - Diary
  - Physics
  - Japanese
  - Journal club
---
昨日月曜日のニューイングランドは大変な[吹雪](https://www.cbsnews.com/boston/news/boston-blizzard-massachusetts-snow-blizzard-of-2026/)だった。今朝起きてみると、屋根のあるはずの我が家のベランダにも大量の雪が吹き込み、足を踏み入れたらしっかり沈み込む程の雪が積もっていた。月曜日のお昼には、[Chez Pierre Seminar](https://physics.mit.edu/events/chez-pierre-seminar-series/)というCondensed Matter groupによるセミナーが毎週行われるのだが、そのセミナーも明日水曜日に延期となった。

延期となったセミナーはEthan Lake[^1]によるものである。彼は3年ほど前にMITでSenthil TodadriのもとでPhDを取得後、現在はUC BerkeleyのMiller Fellowポスドクをしている。私がPhD一年目のときにはEthan LakeはまだMITの学生で、私がPhD一年目で取った授業 Theory of solids のTAをやっていた。そのとき彼のrecitationの授業を受けたことがあり、とてもわかり易かったのが記憶に残っている。当時彼のPhD Defenseも聞きに行ったが、これまた非常にわかりやすい発表だった。彼の卒業後、一度研究会で発表を聞いたこともある。そのときの発表は、非平衡状態から平衡状態への緩和を計算のアルゴリズムだと捉えて（は？）、CSの複雑性やアルゴリズムの知見を使って緩和時間を議論する（は？）というとんでもないアイディアの話だった（[論文](https://journals.aps.org/prx/abstract/10.1103/PhysRevX.14.021034)はPRXに出ていた）。この発表もまた非常にわかりやすく、本当に感銘を受けた。もちろんすべての証明を追うのはとても私には無理だが、とにかく一年以上前に聞いたこの発表の内容をこれくらい自分で思い出せる程度には私でも理解できる発表だった。彼は、学生だった時代を私が知っている人の中で、最も独創的で面白い研究者だと思う。

[^1]:[彼のWebsite](https://ethanlake.github.io/)も面白い。私のお気に入りはFunページにある"30 days of date problems"。

今回の彼のセミナーは、通常のChez Pierreではなく、**Special** Chez Pierre Seminarである。特に今回の場合には何を意味するかというと、事実上のJob interviewと思われる。要するに、MITのCondensed matter theoryの新しいAssistant Professorを選ぶためのものである。すでにいくつかのSpecial Chez Pierre Seminarが行われており、これらの中から次のAssistant Professorが選ばれるのだろう。個人的には、Ethan Lakeが候補者に選ばれたのは至極納得の人選だと思う。

さて、彼の明日のセミナーのタイトルは"Many-body memories"である。以下がその発表要旨の引用である：

> Speaker: Ethan Lake, UC Berkeley
> 
> Title: “Many-body memories”
> 
> Abstract: Are there many-body systems capable of retaining long-term memory of their initial conditions, even when coupled to a noisy environment? This question is central to a wide range of problems in nonequilibrium dynamics, condensed matter physics, and applied quantum science, and we are only just beginning to answer it. In this talk, I will overview recent progress in this direction, for both classical and quantum information. On the classical side, I will describe spin systems that encode information in a self-organising, noise-robust way. Studying these systems has led to new discoveries in nonequilibrium statistical physics, and has demonstrated that achieving order in the absence of any symmetry may be easier than previously thought. On the quantum side, I will present many-body systems whose native dynamics autonomously protects quantum information against decoherence. These systems have the potential to significantly streamline experimental quantum error correction efforts, and define a new direction in the classification of nonequilibrium phases of quantum matter

もうアブストからして面白そう。まだ聞いてないから知らんけど。気になったので、試しに彼の最近の論文を見てみることにした。彼のGoogle Scholarから、関連してそうな最近の論文として"[Exploring the Landscape of Nonequilibrium Memories with Neural Cellular Automata](https://journals.aps.org/prl/abstract/10.1103/2f97-49t1)"(arXiv版は[これ](https://arxiv.org/abs/2508.15726))を見つけたので読んでみた。

非平衡物理もCellular Automataとやらも何も知らないド素人の感想としては、めちゃくちゃ面白かった。まずそもそも、論文がとてもわかり易い。私は専門家でも何でもないのに論文の内容がほぼ完全に理解できる。次に、問題提起もシンプルで明確である。ノイズの下でも情報を保持できるような、robustなmany-body memoryがどう実現できるかという問いは、非常にシンプルでわかりやすく、かつ物理としても基本的で重要な問題である。その問題へのアプローチも見事だ。Cell Automataというシンプルなモデル群で非常にシンプルなmany-body memoryを定義し、さらにそれを機械学習を使って様々なモデルを数値計算で探索、どんなmemoryが実現しうるのかを調べている。そしてその結果、Noise-stabilized orderという新たな現象を発見した。このNoise-stabilized orderがどのように理解できるのかについてはまた別の[論文](http://arxiv.org/abs/2509.20730)があるようで、少しだけ覗いてみたがこちらも面白そうである。

まだセミナーを聞いてもいないのに、「なるほどこれが新しい物理を創り出すということか」と深く感銘を受けてしまった。こういう研究を自分でもやってみたいものだ。


