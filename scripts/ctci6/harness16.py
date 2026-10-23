"""Reuse the typed, expected-answer-free submission adapter."""
from harness08_typed import source as typed_source

def source(language,starters=False,only_ref=None):
    return typed_source(language,starters,only_ref,staging_name='staged16')
