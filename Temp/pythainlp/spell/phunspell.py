# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Phunspell

A pure Python spell checker utilizing spylls, a port of Hunspell.

:See Also:
    * \
        https://github.com/dvwright/phunspell
"""
from typing import List
import phunspell

pspell = phunspell.Phunspell("th_TH")


def spell(text: str) -> List[str]:
    return list(pspell.suggest(text))


def correct(text: str) -> str:
    return list(pspell.suggest(text))[0]
