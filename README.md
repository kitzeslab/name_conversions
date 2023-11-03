# name_conversions
Convert between bird species names: scientific names, English common names, and IBP or BBL 4-letter alpha codes

Or, use the tables of name equivalence from `/resources` directly.

## Example usage:
```python
import name_conversions
scientific = name_conversions.alpha_to_sci('NOCA') #also works with 'noca'
alpha = name_conversions.common_to_alpha('Cardinalis cardinalis') #also works with "cardinalis-cardinalis"
common = name_conversions.alpha_to_common('NOCA')
#etc
```

## Function list:
```
 'alpha_to_common',
 'alpha_to_sci',
 'bn_common_to_sci',
 'common_to_alpha',
 'common_to_sci',
 'sci_to_alpha',
 'sci_to_bn_common',
 'sci_to_xc_common',
 'xc_common_to_sci'
 'get_species_list',
```

## Installation
Clone this repository then run `pip install /path/to/cloned/name_conversions` in the command line in your Python environment. 
