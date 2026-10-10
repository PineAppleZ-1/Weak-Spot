"""Word bank for Weak Spot.

A broad mix of everyday words, plus extra words packed with the letters people
usually struggle with (q, z, x, j, k, v, y) so the AI always has something to
target. Add your own words to RAW_WORDS: anything 3-11 letters, a-z only.
"""

RAW_WORDS = """
able about above accept across action actually address admit adult affect after
again agency agent agree ahead allow almost alone along already also always
amazing among amount animal another answer anyone appear apply approach area
argue around arrive article artist assume attention author avoid away baby back
balance bank base beach beautiful because become before begin behind believe
benefit best better between beyond bill bird black blue board body book born
both bottle brain branch bread break bridge bright bring brother brown budget
build building business butter button cable call camera candle capital card
care career carry castle catch cause center century certain chair challenge
chance change chapter charge check cheese chicken child choice choose circle
city claim class clean clear climb clock close cloud coach coast coffee cold
collect college color common company compare computer concern condition consider
continue control cook copper corner cost cotton could country couple course
cover create credit culture current curtain customer dance danger dark data
daughter decade decide decision deep degree describe desert design detail
develop diamond different difficult dinner direct discover dinosaur doctor
dollar dolphin door double dragon drawer dream dress drink drive during each
early earth east easy edge effect effort eight either electric elephant else
energy engine enjoy enough enter entire equal evening event every evidence
exactly example exist expect explain eye face fact factory family famous far
farm fast father feather feel field fight figure fill film final finally find
finger finish fire first fish five flag flash floor flower focus follow forest
forget form forward four free fresh friend front fruit full funny future galaxy
game garden gentle giant gift girl give glass global glove goal gold good great
green ground group grow guess guitar habit hair half hammer hand happen happy
harbor hard harvest have head health hear heart heavy hello help here hidden
high history hold holiday home honey hope horse hospital hotel hour house
however huge human humor hundred hungry idea image imagine impact important
improve include increase indeed island issue item itself join just keep kind
kitchen know ladder land language large laser last late laugh lead leader learn
least leave lemon less letter level library life light like likely line lion
list listen little live local long look lose loud love lucky lunch machine magic
magnet main major make manage many map market marble master matter maybe meadow
mean measure media medal meet member memory message metal method middle might
million mind minute mirror model modern moment money month moon more morning
most mother motion mountain mouse mouth move movie much music name nation
nature near need network never news next nice night noble north note nothing
notice number ocean offer office often okay once only open orange orbit order
other outside over owner page paint palace paper parent park part party pass
past pattern pause peace pencil people pepper perfect perhaps period person
phone picture piece pilot place planet plant plastic play player please plenty
point policy polite popular position possible potato power practice prepare
present pretty price print private problem process produce product program
project promise protect proud provide public pull purple purpose push quality
question quickly quite rabbit race radio rain raise range rather reach read
ready real reason receive recent record reduce region remain remember repeat
report rescue result return reveal ribbon rich right river road robot rock role
room round rule safe sail salad same sample sand save scene school science score
screen search season second secret section seed seem sell send sense serious
serve service seven several shadow shape share shell shine shore short should
shoulder show side sign signal silent silver similar simple since sing single
sister size skill sleep slow small smile smooth snack snow social soft solid
some someone something sometimes song soon sound source south space speak
special speed spend spirit spring square stage stand star start state station
stay step still stone stop store storm story strange street strong student study
style subject success sudden sugar summer sun support sure surface surprise
sweet swim system table take talent talk task teach teacher team tell temple
tend term test than thank that their them theory there these thing think third
this those though thought thousand three through throw ticket tiger time tiny
today together tomato tonight tooth topic total touch toward tower town trade
train travel treasure treat tree trip true truth try tunnel turn turtle twelve
type umbrella uncle under unit until upon useful usual valley value various very
view village visit voice wait walk wall want warm watch water wave wear weather
week weight well west whale what wheel when where whether which while whisper
white whole wide wild will window winter wish with within without wonder wood
word work world worry would write wrong yard year yellow young youth
quick quiet quote quest queen quiz squad equip liquid unique query quilt quarter
squirrel squash request require quarrel banquet frequent conquer
zebra zero zone zoom lazy dozen puzzle frozen breeze jazz pizza blaze amaze maze
prize freeze crazy fizz zipper wizard ozone hazard horizon citizen gazebo zigzag
bronze glaze dizzy fuzzy sizzle buzz zest zinc
box fox mix fix tax wax next text exit exam extra expert taxi oxygen relax index
complex luxury maximum exotic explore express extend vortex climax sixty toxic
jump jacket joke journey judge juice jungle junior jelly object enjoy reject
jewel banjo pajama jigsaw jogging justice jealous jolly jovial juggle javelin
kayak knife knock kitten kick kiosk karate ketchup kingdom kettle awkward
blanket monkey pocket rocket sketch hockey quirky kidney keyboard kangaroo
vivid velvet valve vacuum vanish vapor victory violin vintage volcano voyage
yawn yoga yogurt yesterday mystery rhythm crystal oyster yacht sky
"""

WORDS = sorted({w for w in RAW_WORDS.split() if w.isalpha() and 3 <= len(w) <= 11})
