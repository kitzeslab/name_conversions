import name_conversions
import pytest


def test_get_species_list():
    assert len(name_conversions.get_species_list()) > 0


def test_sci_to_bn_common():
    sp = name_conversions.get_species_list()[0]
    name_conversions.sci_to_bn_common(sp)


def test_sci_to_xc_common():
    sp = name_conversions.get_species_list()[0]
    name_conversions.sci_to_xc_common(sp)


def test_xc_common_to_sci():
    common = name_conversions.sci_to_xc_common(name_conversions.get_species_list()[0])
    name_conversions.xc_common_to_sci(common)


def test_bn_common_to_sci():
    common = name_conversions.sci_to_bn_common(name_conversions.get_species_list()[0])
    name_conversions.bn_common_to_sci(common)


def test_common_to_sci():
    common = name_conversions.sci_to_bn_common(name_conversions.get_species_list()[0])
    name_conversions.common_to_sci(common)


def test_alpha_to_common():
    common = "Northern Cardinal"

    for alpha in ("NOCA", "noca", "nocA"):
        assert name_conversions.alpha_to_common(alpha, "bbl") == common
        assert name_conversions.alpha_to_common(alpha, "ibp") == common


def test_alpha_to_sci():
    scientific = "Cardinalis cardinalis"

    for alpha in ("NOCA", "noca", "nocA"):
        assert name_conversions.alpha_to_sci(alpha, "bbl") == scientific
        assert name_conversions.alpha_to_sci(alpha, "ibp") == scientific


def test_common_to_alpha():
    alpha = "NOCA"

    for common in ("Northern Cardinal", "northern cardinal", "northern-cardinal"):
        assert name_conversions.common_to_alpha(common, "bbl") == alpha
        assert name_conversions.common_to_alpha(common, "ibp") == alpha


def test_sci_to_alpha():
    alpha = "NOCA"

    for scientific in ("Cardinalis cardinalis", "cardinalis-cardinalis"):
        assert name_conversions.sci_to_alpha(scientific, "bbl") == alpha
        assert name_conversions.sci_to_alpha(scientific, "ibp") == alpha


def test_ebird_to_sci():
    ebird_code = "norcar"
    assert name_conversions.ebird_to_sci(ebird_code) == "Cardinalis cardinalis"


def test_ebird_to_common():
    ebird_code = "norcar"
    assert name_conversions.ebird_to_common(ebird_code) == "Northern Cardinal"


def test_switch_ebird_taxonomy_year():
    """blttro2 is not in 2023 taxonomy, but is in 2022"""
    name_conversions.switch_ebird_taxonomy_year(2023)
    with pytest.raises(KeyError):
        name_conversions.ebird_to_sci("blttro2")
    name_conversions.switch_ebird_taxonomy_year(2022)
    name_conversions.ebird_to_sci("blttro2")
