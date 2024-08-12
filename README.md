# facere-sensum: make sense of the turmoil

`facere-sensum` is a general-purpose metrics framework designed to quantify anything in a meaningful numerical format. It permits the aggregation of individual metrics to create higher-level metrics that reflect collective behavior with a single indicator.

In practical terms, `facere-sensum` offers a structured approach for product management to establish development priorities and objectives. For development teams, it serves as a tool to pinpoint the specific areas where their efforts should be concentrated to achieve the desired goal.

Comprehensive documentation is available [here](https://lunarserge.github.io/facere-sensum).

# Installation

    pip install facere-sensum

# Usage

    facere_sensum [-h] [--version] [--auth [AUTH]] [--config [CONFIG]] {create,update,chart}

{**create**,**update**,**chart**}: high-level action to perform

Options:
*  **-h**, **--help**:    show help message and exit
*  **--version**:         show the version number and exit
*  **--auth [AUTH]**:     authentication config
*  **--config [CONFIG]**: layer config (default: `config.json`)
