%------------------------------------------------------------------------------%
% Klasa do skladu prac dyplomowych w jezykach: polskim i angielskim na         %
% wydziale Matematyki i Nauk Informacyjnych Politechniki Warszawskiej.         %
% Autor: Kamen Radew <radewk@student.mini.pw.edu.pl>                           %
%------------------------------------------------------------------------------%
\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{mini}[2011/10/15 v0.3 Praca dyplomowa (MiNI PW)]
%------------------------------------------------------------------------------%
\RequirePackage{ifthen}
\newboolean{english}
\setboolean{english}{false}
\newboolean{lady}
\setboolean{lady}{false}
%------------------------------------------------------------------------------%
\DeclareOption{english}{\setboolean{english}{true}}
\DeclareOption{lady}{\setboolean{lady}{true}}
%\DeclareOption{12pt}{\OptionNotUsed}
%\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions\relax
\LoadClass[a4paper,11pt,twoside,onecolumn,openany]{article}
%------------------------------------------------------------------------------%
\RequirePackage{graphicx}
\graphicspath{{graphics/}}
%------------------------------------------------------------------------------%
\RequirePackage{geometry}
\geometry{
  inner=20mm,
  outer=20mm,
  bindingoffset=0mm,
  top=20mm,
  bottom=15mm,  % 20mm
  includeheadfoot
}
%%------------------------------------------------------------------------------%
\pagestyle{plain}
%\RequirePackage{fancyhdr}
%\pagestyle{fancy}
%\fancyhf{}
%\fancyhead[RO,LE]{\slshape\rightmark}
%\fancyhead[LO,RE]{\slshape\leftmark}
%\fancyfoot[C]{\thepage}
%\fancyhead[RE]{\slshape\leftmark}
%\fancyhead[LO]{\slshape\rightmark}
%\fancyhead[LE,RO]{\thepage}
%------------------------------------------------------------------------------%
%\renewcommand{\chaptermark}[1]{\markboth{\thechapter.\enspace#1}{}}
%\renewcommand{\sectionmark}[1]{\markright{\thesection.\enspace#1}}
%------------------------------------------------------------------------------%
%\def\cleardoublepage{\clearpage\if@twoside
%\ifodd\c@page\else\hbox{}\thispagestyle{empty}\newpage
%\if@twocolumn\hbox{}\newpage\fi\fi\fi}
%------------------------------------------------------------------------------%
%\renewcommand{\@seccntformat}[1]{\csname the#1\endcsname.\enspace}
\renewcommand{\numberline}[1]{\hb@xt@\@tempdima{#1.\hfil}}
%------------------------------------------------------------------------------%
\RequirePackage[parfill]{parskip}[2001/04/09]
\RequirePackage{setspace}
\frenchspacing
%------------------------------------------------------------------------------%
\clubpenalty=10000
\widowpenalty=10000
\brokenpenalty=10000
%------------------------------------------------------------------------------%
\RequirePackage{amsmath}
\RequirePackage{amsthm}
\RequirePackage{amsfonts}
\RequirePackage{amssymb}
%------------------------------------------------------------------------------%
\RequirePackage[OT4]{polski}
\bibliographystyle{plplain}
%------------------------------------------------------------------------------%
\RequirePackage[unicode]{hyperref}
\hypersetup{
  bookmarksopen,
  bookmarksopenlevel=1,
  pdfborder={0 0 0},
  pdfdisplaydoctitle,
  pdfpagelayout={SinglePage},
  pdfstartview={FitH}
}
%------------------------------------------------------------------------------%
%\def\@schapter#1{
%\phantomsection\addcontentsline{toc}{chapter}{#1}
%\markboth{#1}{#1}\@makeschapterhead{#1}\@afterheading}
%%------------------------------------------------------------------------------%
%\renewcommand{\tableofcontents}{
%\if@openright\cleardoublepage\else\clearpage\fi\thispagestyle{plain}
%\pdfbookmark[0]{\contentsname}{tableofcontents}
%\@makeschapterhead{\contentsname}\@afterheading
%\@mkboth{\MakeUppercase\contentsname}{\MakeUppercase\contentsname}
%\@starttoc{toc}}
%------------------------------------------------------------------------------%
\def\title#1{\gdef\@title{#1}\hypersetup{pdftitle={#1}}}
\def\@title{\@latex@error{No title given}\@ehc}
\def\titleaux#1{\gdef\@titleaux{#1}}
\def\@titleaux{\@latex@error{No polish title given}\@ehc}
\def\author#1{\gdef\@author{#1}\hypersetup{pdfauthor={#1}}}
\def\@author{\@latex@error{No author given}\@ehc}
\def\coauthor#1{\gdef\@coauthor{#1}}
\def\@coauthor{\@latex@error{No coauthor given}\@ehc}
\def\supervisor#1{\gdef\@supervisor{#1}}
\def\@supervisor{\@latex@error{No supervisor given}\@ehc}
\def\tutor#1{\gdef\@tutor{#1}}
\def\@tutor{\@latex@error{No tutor given}\@ehc}
\def\type#1{\gdef\@type{#1}}
\def\@type{\@latex@error{No type given}\@ehc}
\def\discipline#1{\gdef\@discipline{#1}}
\def\@discipline{\@latex@error{No discipline given}\@ehc}
\def\monthyear#1{\gdef\@monthyear{#1}}
\def\@monthyear{\@latex@error{No month and year given}\@ehc}
\def\date#1{\gdef\@date{#1}}
\def\@date{\@latex@error{No date given}\@ehc}
\def\album#1{\gdef\@album{#1}}
\def\@album{\@latex@error{No album number given}\@ehc}
%------------------------------------------------------------------------------%
\def\@descriptionfirst{}
\def\@descriptionsecond{Raport nr 2}
\def\@pmcap{Student}
\def\@authorcap{Autor}
\def\@location{Warszawa}
\def\@titlepagecap{Strona tytu{\l}owa}
%------------------------------------------------------------------------------%
\def\@definition{Definicja}
\def\@theorem{Twierdzenie}
\def\@lemma{Lemat}
\def\@proposition{Stwierdzenie}
\def\@corollary{Wniosek}
\def\@remark{Uwaga}
\def\@example{Przyk{\l}ad}
%------------------------------------------------------------------------------%
\ifthenelse{\boolean{english}}{
  %-----------------------------------------%
  \def\@definition{Definition}
  \def\@theorem{Theorem}
  \def\@lemma{Lemma}
  \def\@proposition{Proposition}
  \def\@corollary{Corollary}
  \def\@remark{Remark}
  \def\@example{Example}
}{
  \def\bibname{Literatura}
}
%%------------------------------------------------------------------------------%
\newtheoremstyle{thm}{3ex}{3ex}{\itshape}{}{\bfseries}{.}{.5em}{#1 #2\thmnote{ (#3)}}
\newtheoremstyle{rem}{3ex}{3ex}{}{}{\bfseries}{.}{.5em}{#1 #2\thmnote{ (#3)}}
\theoremstyle{thm}
\newtheorem{definition}{\@definition}[section]
\newtheorem{theorem}{\@theorem}[section]
\newtheorem{lemma}[theorem]{\@lemma}
\newtheorem{proposition}[theorem]{\@proposition}
\newtheorem{corollary}[theorem]{\@corollary}
\theoremstyle{rem}
\newtheorem{remark}{\@remark}[section]
\newtheorem{example}{\@example}[section]
\renewcommand{\qedsymbol}{\ensuremath{\blacksquare}}
%------------------------------------------------------------------------------%
\renewcommand{\maketitle}{
\pdfbookmark[0]{\@titlepagecap}{titlepage}
\begin{titlepage}
\begin{center}
  \hfill
  \vspace{30mm}
  {\large
    \MakeUppercase{\@descriptionfirst}
  \par}
  \vfill
  \begin{spacing}{1.3}
    \textbf{\Large\MakeUppercase{\@title}}
    \\
    \MakeUppercase{\@descriptionsecond}
  \end{spacing}
  \vfill
\end{center}
\hspace{.7\textwidth}
\begin{minipage}[t][80mm]{.6\textwidth}
  \textsc{
  \\\\\@authorcap:\\\@author}\par
  \vspace{7mm}
\end{minipage}
\begin{center}
  \textsc{\large\@location, \@monthyear}
\end{center}
\end{titlepage}}
%------------------------------------------------------------------------------
\endinput
