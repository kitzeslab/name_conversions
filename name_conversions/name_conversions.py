"""a set of utilites for converting between scientific and common names of bird species in different
naming systems (xeno canto and bird net)"""
import importlib.resources

import numpy as np
import pandas as pd

with importlib.resources.path("name_conversions.resources", "species_table.csv") as f:
    species_table = pd.read_csv(f)

with importlib.resources.path(
    "name_conversions.resources", "bbl-alpha-codes_2021.csv"
) as f:
    bbl_alpha = pd.read_csv(f)

with importlib.resources.path(
    "name_conversions.resources", "ibp-alpha-codes_2021.csv"
) as f:
    ibp_alpha = pd.read_csv(f)


def get_species_list():
    """returns a list of scientific-names (lowercase-hyphenated) of species"""

    return (
        species_table[["bn_code", "bn_mapping_in_xc_dataset"]]
        .dropna()["bn_mapping_in_xc_dataset"]
        .sort_values()
        .to_list()
    )


name_table_sci_idx = species_table.set_index("scientific", drop=True)
name_table_xc_com_idx = species_table.set_index("xc_common", drop=True)
name_table_bn_com_idx = species_table.set_index("bn_common", drop=True)
ibp_alpha_alpha_idx = ibp_alpha.set_index("true_alpha", drop=True)
bbl_alpha_alpha_idx = bbl_alpha.set_index("true_alpha", drop=True)
ibp_alpha_sci_idx = ibp_alpha.set_index("scientific_name", drop=True)
bbl_alpha_sci_idx = bbl_alpha.set_index("scientific_name", drop=True)
ibp_alpha_com_idx = ibp_alpha.set_index("common_name", drop=True)
bbl_alpha_com_idx = bbl_alpha.set_index("common_name", drop=True)


def sci_to_bn_common(scientific):
    """convert scientific lowercase-hyphenated name to birdnet common name as lowercasenospaces"""
    return name_table_sci_idx.at[scientific, "bn_common"]


def sci_to_xc_common(scientific):
    """convert scientific lowercase-hyphenated name to xeno-canto lowercasenospaces common name"""
    return name_table_sci_idx.at[scientific, "xc_common"]


def xc_common_to_sci(common):
    """convert xeno-canto common name (ignoring dashes/spaces/case) to lowercase-hyphenated name"""
    common = common.lower().replace(" ", "").replace("-", "")
    return name_table_xc_com_idx.at[common, "scientific"]


def bn_common_to_sci(common):
    """convert bird net common name (ignoring dashes, spaces, case) to lowercase-hyphenated name"""
    common = common.lower().replace(" ", "").replace("-", "")
    return name_table_bn_com_idx.at[common, "scientific"]


def common_to_sci(common):
    """convert bird net common name to scientific name as lowercase-hyphenated

    Ignores dashes, spaces, case
    """
    return bn_common_to_sci(common)


def alpha_to_common(alpha, alpha_type="ibp"):
    """convert alpha code to common name; use BBL or IBP alpha codes

    Args:
        alpha: 4-letter alpha code (will be converted to uppercase)
        alpha_type: 'bbl' or 'ibp'
    """
    assert isinstance(alpha, str) and len(alpha) == 4, "alpha must be a 4 letter string"
    if alpha_type == "bbl":
        return bbl_alpha_alpha_idx.at[alpha.upper(), "common_name"]
    elif alpha_type == "ibp":
        return ibp_alpha_alpha_idx.at[alpha.upper(), "common_name"]
    else:
        raise ValueError("alpha_type must be 'bbl' or 'ibp'")


def alpha_to_sci(alpha, alpha_type="ibp"):
    """convert alpha code to scientific name; use BBL or IBP alpha codes

    Args:
        alpha: 4-letter alpha code (will be converted to uppercase)
        alpha_type: 'bbl' or 'ibp'
    """
    assert isinstance(alpha, str) and len(alpha) == 4, "alpha must be a 4 letter string"
    if alpha_type == "bbl":
        return bbl_alpha_alpha_idx.at[alpha.upper(), "scientific_name"]
    elif alpha_type == "ibp":
        return ibp_alpha_alpha_idx.at[alpha.upper(), "scientific_name"]
    else:
        raise ValueError("alpha_type must be 'bbl' or 'ibp'")


def common_to_alpha(common, alpha_type="ibp", flexible_match=True):
    """convert common name to alpha code; use BBL or IBP alpha codes

    Common name must match case and syntax exactly, for instance "Red-necked Grebe"

    Args:
        common: common name
            Note: if flexible_match is False, case and syntax must match
            exactly, for instance "Red-necked Grebe"
        alpha_type: 'bbl' or 'ibp'
        flexible_match: if True, case and syntax of `common` are ignored
            (converts `common` to lowercase letters only string)

    """
    import re

    assert alpha_type.lower() in ("bbl", "ibp"), "alpha_type must be 'bbl' or 'ibp'"
    table = bbl_alpha_com_idx if alpha_type.lower() == "bbl" else ibp_alpha_com_idx

    if flexible_match:
        common = re.sub("[^a-zA-Z]", "", common).lower()

        idx = table.index.str.replace("[^a-zA-Z]", "", regex=True).str.lower()
        return table.iloc[idx.get_loc(common)]["true_alpha"]
    else:
        return table.at[common, "true_alpha"]


def sci_to_alpha(sci, alpha_type="ibp", flexible_match=True):
    """convert scientific name to alpha code; use BBL or IBP alpha codes

    Args:
        sci: scientific name
            Note: if flexible_match is False, must match string exactly,
            for instance "Bubo virginianus"
        alpha_type: 'bbl' or 'ibp'
        flexible_match: if True, converts "-" to space, first letter to uppercase,
            and rest to lowercase.
            This assists in matching the format "Genus species" eg "Crux crux"
            default: True
    """
    assert alpha_type.lower() in ("bbl", "ibp"), "alpha_type must be 'bbl' or 'ibp'"

    table = bbl_alpha_sci_idx if alpha_type.lower() == "bbl" else ibp_alpha_sci_idx

    if flexible_match:
        sci = sci.replace("-", " ")
        sci = sci[0].upper() + sci[1:].lower()

    return table.at[sci, "true_alpha"]
