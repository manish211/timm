fx(broken, [0    ]).
fx(hurt,   [0,0,1]).
fx(helped, [0,1,1]).
fx(made,   [1    ]).

:- op(1,xfx,by).

by(Goal,W) :-
  by(made,Goal,[],W).

by(Op,Goal) --> 
  is(Goal=Want), {want(Op,Want)}, abduce(Goal).

is(X=Y,W0,W) :- less(W0,X=Z,W) -> Z=Y; W=[X=Y|W0].

less([H|T],  H, T).
less([H1|T1],H2,[H1|T2]) :- less(T1,H2,T2).

want(X,Y) :- fx(X,L), within(Y,L).

within(Item,L) :-
  var(Item)
  -> setof(N/X, (member(X,L),N is random(100000)),L1),
     member(_/Item,L1)
  ; member(Item,L).

abduce(Goal,W0,W) :-
  functor(Blank,Goal,2),
  clause(Blank,_) 
  -> Todo =.. [Goal,W0,W],
     Todo 
   ; W0=W.

goodBrowser -->
   made by performance,
   made by userFriendly,
   made by security.

performance -->
   made by speed, 
   made by stability.

speed -->
   made   by opera,
   hurt   by ie,
   broken by netscape.

stability -->
   helped by opera,
   hurt   by tmp1,
   broken by netscape.

tmp1 -->
   made   by ie,
   helped by crashesMyPc.

userFriendly -->
    hurt  by opera,
    made  by ie.

security -->
   hurt   by opera,
   broken by ie,
   broken by netscape.

%makes > helps > hurts >breaks
