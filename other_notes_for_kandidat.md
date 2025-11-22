### Skriv om detta i uppsatsen ###

🧠 Problemet: LLM + många fält = svårt

När du ger modellen:

10 frågor

10 möjliga tool-calls

10 möjliga next steps

…så måste modellen hålla:

Vad som redan är besvarat

Vad som saknas

Vilket som är logiskt nästa

När tool ska triggas eller inte

När den ska skriva text vs. funktion
 
Och den har ingen persistent intern state.
Den måste deducera allt via prompt + history.
Det blir snabbt förvirrat, repetitivt eller inkonsekvent.

Det är därför extremt få LLM-tillämpningar låter modellen styra “hela flödet själv”.