"""Reuse the existing probability-interval/die engine for small subset masks.

Compatible increasing occurrence labelings lift an observable duplicate-valued
subsequence uniformly to masks. Thus a uniform lifted mask is equivalent to the
required aggregate subset law, without requiring a particular coin mapping.
Large inputs get structural, inclusion and size-moment checks; finite checks are
not a universal probability proof. The independently authored references have
an all-n proof from one independent coin per occurrence.
"""
import importlib
import re
from harness_rand16 import parts as dice_parts
from models_rand16 import RAND5

SIZE={'python':'len(SubsetState13.Input)','javascript':'SubsetState13.Input.length','csharp':'SubsetState13.Input.Length','java':'SubsetState13.Input.length','cpp':'static_cast<int>(SubsetState13::Input.size())'}
def parts(language,code):
    module=importlib.import_module('harness_subset13_'+language)
    core=RAND5[language].replace('Rand5Source','ChoiceBitSource')+module.CORE
    value,inside=dice_parts(language,code+'\n'+core)
    value=value.replace('Solution_16_23','SubsetSubject13').replace('UniformSeven','ChooseMask13').replace('Rand5Source','ChoiceBitSource').replace('RandomAudit16','SubsetAudit13').replace('executeRand16','executeSubset13').replace('ExecuteRand16','ExecuteSubset13')
    inside=inside.replace('RandomAudit16','SubsetAudit13').replace('ExecuteRand16','ExecuteSubset13').replace('executeRand16','executeSubset13')
    size=SIZE[language]
    # The engine's die is now a lifted subset mask and its primitive is one bit.
    value=value.replace('maximum = 7 if Mode == "rand5" else 5','maximum = 2').replace('outcomes = 5 if Mode == "rand5" else 7','outcomes = 1 << '+size)
    value=value.replace("maximum = Mode === 'rand5' ? 7 : 5",'maximum = 2').replace("outcomes = Mode === 'rand5' ? 5 : 7",'outcomes = 1 << '+size)
    value=value.replace('maximum = Mode == "rand5" ? 7 : 5','maximum = 2').replace('outcomes = Mode == "rand5" ? 5 : 7','outcomes = 1 << '+size)
    value=value.replace('maximum=Mode.equals("rand5")?7:5','maximum=2').replace('outcomes=Mode.equals("rand5")?5:7','outcomes=1 << '+size)
    value=value.replace('Draw(1,5)-1','Draw(1,2)-1').replace('Draw.applyAsInt(1,5)-1','Draw.applyAsInt(1,2)-1').replace('Draw(1, 5) - 1','Draw(1, 2) - 1')
    value=value.replace('0<=value<=6','0<=value<(1<<'+size+')').replace('0 <= value <= 6','0 <= value < (1 << '+size+')')
    value=value.replace('value>=0&&value<=6','value>=0&&value<(1<<'+size+')')
    value=re.sub(r'draws\s*>\s*0',lambda m:'('+size+('==0 or draws>0)' if language=='python' else '==0||draws>0)'),value)
    value=re.sub(r'(draws(?:\[0\])?\s*<=\s*)128',lambda m:m[1]+'(128*'+size+'+256)',value)
    value=re.sub(r"<\s*40(?=,\s*[\"']Seeded die distribution)", '<4*(outcomes-1)+80',value)
    value=value.replace('false,5,7','false,2,1<<'+size)
    value=module.finish(value)
    value=value.replace('Die transformation is biased','Returned subsets are biased').replace('die distribution','subset distribution').replace('die outputs','subset outputs').replace('die triples','subset triples').replace('die pairs','subset pairs')
    value=value.replace('with two Rand5 draws per attempt','for independent inclusion decisions').replace('die result','subset observation').replace('die face','sampled subset').replace('Die result','Subset observation')
    return value,inside
