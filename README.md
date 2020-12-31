# Analyzing Batting Positions in Test Cricket 

Ian Chappell [claims](https://www.espncricinfo.com/story/why-are-steven-smith-and-joe-root-so-averse-to-batting-at-no-3-1223440) that Steven Smith and Joe Root would be better off batting at 3. I tested his claim using match data from ESPNCricinfo's Statsguru. In a nutshell, neither Australia nor England is measurably more successful when their star batsmen come in at 3 rather than 4.

## England and Root

At first glance, England's average totals don't change much whether Root bats at 3 or 4. 
[England Totals Boxplot](./eng_totals_boxplot.png)

An interaction plot confirms the intuition; the 95% confidence intervals for England's expected score overlap for every innings, suggesting no significant difference.
[England Totals Interaction Plot](./eng_totals_interaction.png)

## Australia and Smith

Australia's scores vary slightly more, but still not as much as Chappell might expect. 
[Australia Totals Boxplot](./aus_totals_boxplot.png)

In any case, the two-way ANOVA in `analysis.py` finds no significant correlation between Smith'sposition and Australia's score. 
[Australia Totals Interaction Plot](./aus_totals_interaction.png)
