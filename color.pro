
 	
/k {
  false BG
  0 0 0.9 FG
%Face: Keyword Courier bfs
  Show
} bind def

/K {
  false BG
  0 0 0.8 FG
%Face: Keyword_strong Courier-Bold bfs
  Show
} bind def

and turn it into:
 	
/k {
  0.2 1 0.2 true BG
  1 0.2 1 FG
%Face: Keyword Helvetica bfs
  Show
} bind def

/K {
  0.4 0.2 0 true BG
  0.5 1 1 FG
%Face: Keyword_strong Times-BoldItalic bfs
  Show
} bind def
