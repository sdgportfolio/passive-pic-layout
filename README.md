# Parametric Passive PIC Layouts

A growing collection of parameterized GDSII layout generators for passive photonic and resonant structures, developed in Python using [GDSFactory](https://gdsfactory.github.io/gdsfactory/) and inspected in [KLayout](https://www.klayout.de/).

This project demonstrates reusable component generation, hierarchical layout, layer management, geometry validation, and automated GDSII export.

## Components

| Component | Description | Status |
|---|---|---|
| [Split-Ring Resonator](srr/) | Parameterized SRR with a separately defined material-flake footprint centered over its capacitive gap | Complete |
| [Mach–Zehnder Interferometer](mzi/) | Asymmetric MZI wavelength-demultiplexer layout targeting 1548 nm and 1550 nm | Planned |
| [Multimode Interference Coupler](mmi/) | 1×4 MMI splitter layout targeting equal power distribution across four output ports | Planned |

## Repository Structure

```text
passive-pic-layout/
├── README.md
├── LICENSE
├── srr/
│   ├── README.md
│   ├── requirements.txt
│   ├── srr_with_flake.py
│   ├── srr_with_flake.gds
│   └── srr_with_flake_klayout.png
├── mzi/
│   └── README.md
└── mmi/
    └── README.md
```

The MZI and MMI directories will be expanded as their implementations are completed.

## Split-Ring Resonator

The completed SRR project generates a square split-ring resonator with a flake positioned over its capacitive gap. The resonator dimensions, gap size, flake size, and GDS layers can be adjusted through function arguments.

The layout supports an electromagnetic study of a gold split-ring resonator coupled to a van der Waals NbOI₂ flake. The resonator dimensions can be varied to investigate resonance tuning and electromagnetic-field confinement near the capacitive gap. This study was performed in COMSOL and the results have not been uploaded to GitHub.

### Features

- Parameterized resonator and flake dimensions
- Independent GDS layers for the resonator and flake
- Geometry checks for invalid parameter combinations
- Automatic GDSII generation
- KLayout-compatible output
- Component metadata for tracking design parameters

See the [SRR documentation](srr/README.md) for its dimensions, layer map, usage instructions, and generated layout.

## Planned Mach–Zehnder Interferometer

The MZI project will implement an asymmetric Mach–Zehnder interferometer for wavelength demultiplexing. The path-length difference and routing geometry will be parameterized for operation around 1548 nm and 1550 nm.

### Planned Features

- Parameterized arm-length difference
- 1×2 splitter and 2×2 combiner integration
- Automated optical routing
- Optical ports for circuit assembly
- Path-length reporting
- Layout verification
- GDSII export

## Planned 1×4 MMI Splitter

The MMI project will implement a 1×4 multimode-interference splitter designed to distribute the input optical power equally among four output waveguides.

### Planned Features

- Parameterized multimode-region dimensions
- Symmetric four-port output placement
- Input and output taper generation
- Optical ports for higher-level PIC integration
- Layout variants for design sweeps
- GDSII export

## Getting Started

Clone the repository:

```bash
git clone https://github.com/sdgportfolio/passive-pic-layout.git
cd passive-pic-layout
```

Install the dependencies for the component you want to generate. For the SRR:

```bash
python -m pip install -r srr/requirements.txt
```

Generate the default SRR layout:

```bash
python srr/srr_with_flake.py
```

The script exports a GDSII file that can be opened and inspected in KLayout.

## Design Scope

The layouts use illustrative layer assignments and are not tied to a specific foundry process-design kit.

The geometry-validation functions check component parameters and prevent invalid dimensional combinations. They do not replace a foundry-qualified design-rule check.

Fabrication requires:

- Mapping the generic layers to the selected fabrication process
- Applying the appropriate minimum-feature and spacing rules
- Accounting for fabrication bias and process tolerances
- Running the foundry-provided DRC and verification flow

The target optical performance of the MZI and MMI must also be confirmed through electromagnetic or photonic-circuit simulation before fabrication.

## Tools

- Python
- GDSFactory
- KLayout
- GDSII
- Git and GitHub

## Roadmap

- [x] Parameterized SRR with flake
- [x] SRR geometry validation and GDSII export
- [ ] 1548/1550 nm MZI demultiplexer layout
- [ ] 1×4 equal-power MMI splitter layout
- [ ] Continuous-integration checks

## License

This project is available under the terms of the [MIT License](LICENSE).

## Author

**Shroyon Dasgupta**

[GitHub](https://github.com/sdgportfolio)
