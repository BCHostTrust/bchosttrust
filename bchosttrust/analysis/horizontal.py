# bchosttrust/bchosttrust/analysis/horizontal.py
"""Perform horizontal compare"""

import typing
from typing import Literal
from difflib import SequenceMatcher

# https://stackoverflow.com/a/17388505
# License: https://creativecommons.org/licenses/by-sa/3.0/


def _similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


DEFAULT_MIN_RATIO = 0.7


def iter_simular_names(
        from_name: str,
        list_names: typing.Iterable[str],
        min_ratio: float = DEFAULT_MIN_RATIO) -> typing.Generator[str, None, None]:
    """Yields simular strings when comparing from_name again list_names.

    Parameters
    ----------
    from_name : str
        The name checking against other strings
    list_names : typing.Iterable[str]
        The strings to be checked against
    min_ratio : float, optional
        The minimum value returned by SequenceMatcher().ratio(), by default 0.6

    Yields
    ------
    str
        similar strings, not including itself
    """

    for name in list_names:
        if name == from_name:
            continue
        if _similar(from_name, name) > min_ratio:
            yield name


def get_simular_names(
        from_name: str,
        list_names: typing.Iterable[str],
        min_ratio: float = DEFAULT_MIN_RATIO) -> tuple[str]:
    """Get a tuple of simular strings when comparing from_name again list_names.

    Parameters
    ----------
    from_name : str
        The name checking against other strings
    list_names : typing.Iterable[str]
        The strings to be checked against
    min_ratio : float, optional
        The minimum value returned by SequenceMatcher().ratio(), by default 0.6

    Returns
    -------
    tuple[str]
        A tuple of similar strings, not including itself
    """

    return tuple(iter_simular_names(from_name, list_names, min_ratio))


# Currently these values are small, can be extended
DEFAULT_SUS = 30
DEFAULT_BAD = 50


class ThresholdDict(typing.TypedDict):
    """Class of thresholds"""

    SUS: int
    BAD: int


def analyse_domain_name(
        from_name: str,
        ratings: dict[str, int],
        min_ratio: float = DEFAULT_MIN_RATIO,
        sus_threshold: int = DEFAULT_SUS,
        bad_threshold: int = DEFAULT_BAD) -> dict[Literal["HIGH", "LOW"],
                                                  dict[Literal["SUS", "BAD"], set[str]]]:
    """Get lists of similar hostname that are having distinct differences

    Parameters
    ----------
    from_name : str
        The domain checking against other domains
    ratings : dict[str, int]
        Return value of search.get_website_rating, including from_name
    min_ratio : float
        The minimum value returned by SequenceMatcher().ratio(), by default 0.6
    sus_threshold : int
        The difference between rating[from_name] and rating[other] for it
        to start being recognized as suspicious
    bad_threshold : int
        The difference between rating[from_name] and rating[other] for it
        to start being recognized as bad

    Returns
    -------
    dict[Literal["HIGH", "LOW"], dict[Literal["SUS", "BAD"], set[str]]]
        The lists in the folowing hierarchy:
        {
            "HIGHER": {
                "SUS": set(),
                "BAD": set()
            },
            "LOWER": {
                "SUS": set(),
                "BAD": set()
            }
        }
    """

    compare_results = {
        "HIGHER": {
            "SUS": set(),
            "BAD": set()
        },
        "LOWER": {
            "SUS": set(),
            "BAD": set()
        }
    }
    for names in iter_simular_names(from_name, ratings.keys(), min_ratio):
        # If from_name is not trustworthy than names,
        # This would be positive.
        difference = ratings[from_name] - ratings[names]
        if difference > sus_threshold:
            if difference > bad_threshold:
                compare_results["HIGHER"]["BAD"].add(names)
            else:
                compare_results["HIGHER"]["SUS"].add(names)
        elif difference < (sus_threshold * -1):
            if difference > (bad_threshold * -1):
                compare_results["LOWER"]["BAD"].add(names)
            else:
                compare_results["LOWER"]["SUS"].add(names)
    return compare_results
