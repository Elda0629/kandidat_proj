# MEDICAL DEVICE CLASSIFICATION RULES - CODE GENERATION OPTIMIZED

## DEFINITIONS AND CONSTANTS

### Duration Categories
- **TRANSIENT**: Use duration < 60 minutes
- **SHORT_TERM**: Use duration between 60 minutes and 30 days
- **LONG_TERM**: Use duration > 30 days

### Device Type Categories
- **NON_INVASIVE**: Does not penetrate body surface
- **INVASIVE_BODY_ORIFICE**: Penetrates body orifice (not surgical)
- **SURGICALLY_INVASIVE**: Penetrates body surface via surgical means
- **IMPLANTABLE**: Remains in body after procedure
- **ACTIVE**: Relies on electrical/other energy source (not gravity/body)

### Body Contact Locations
- **ORAL_PHARYNX**: Oral cavity to pharynx
- **EAR_CANAL**: Up to ear drum
- **NASAL_CAVITY**: Nasal cavity
- **HEART**: Heart tissue
- **CENTRAL_CIRCULATORY**: Central circulatory system
- **CENTRAL_NERVOUS**: Central nervous system
- **TEETH**: Dental tissue
- **INTACT_SKIN**: Unbroken skin surface
- **INJURED_SKIN**: Broken/wounded skin
- **MUCOUS_MEMBRANE**: Mucous membrane tissue

### Classification Outputs
- **CLASS_I**: Lowest risk
- **CLASS_IIA**: Low-medium risk
- **CLASS_IIB**: Medium-high risk
- **CLASS_III**: Highest risk

---

## RULE APPLICATION ORDER

Rules should be evaluated in the following order:
1. Special Rules (14-22) - Check first as they override general rules
2. Active Device Rules (9-13)
3. Invasive Device Rules (5-8)
4. Non-Invasive Device Rules (1-4)

---

## NON-INVASIVE DEVICE RULES (1-4)

### RULE 1: Default Non-Invasive Classification
```
IF device_type == NON_INVASIVE
   AND no_other_rules_apply:
   RETURN CLASS_I
```

### RULE 2: Non-Invasive Channelling/Storing Devices
```
IF device_type == NON_INVASIVE
   AND (channels OR stores) ANY OF [blood, body_liquids, cells, tissues, liquids, gases]
   AND purpose == eventual_infusion_or_administration_into_body:
   
   IF connected_to_device_class IN [CLASS_IIA, CLASS_IIB, CLASS_III]:
      RETURN CLASS_IIA
   
   ELIF use_case IN [channelling_blood, storing_blood, storing_body_liquids, 
                     storing_organs, storing_organ_parts, storing_cells, storing_tissues]:
      IF device_type == blood_bag:
         RETURN CLASS_IIB
      ELSE:
         RETURN CLASS_IIA
   
   ELSE:
      RETURN CLASS_I
```

### RULE 3: Non-Invasive Modifying Devices
```
IF device_type == NON_INVASIVE
   AND modifies ANY OF [biological_composition, chemical_composition]
   AND target IN [human_tissues, cells, blood, body_liquids, implantation_liquids]:
   
   IF treatment_type IN [filtration, centrifugation, gas_exchange, heat_exchange]:
      RETURN CLASS_IIA
   ELSE:
      RETURN CLASS_IIB

IF device_type == NON_INVASIVE
   AND consists_of == substance_or_mixture
   AND use == in_vitro
   AND contact_with IN [human_cells, human_tissues, human_organs, human_embryos]
   AND application IN [before_implantation, before_administration]:
   RETURN CLASS_III
```

### RULE 4: Non-Invasive Contact with Injured Skin/Mucous Membrane
```
IF device_type == NON_INVASIVE
   AND contacts ANY OF [injured_skin, injured_mucous_membrane]:
   
   IF purpose IN [mechanical_barrier, compression, absorption_of_exudates]:
      RETURN CLASS_I
   
   ELIF injury_type == breached_dermis OR healing_type == secondary_intent:
      RETURN CLASS_IIB
   
   ELIF purpose == manage_micro_environment:
      RETURN CLASS_IIA
   
   ELSE:
      RETURN CLASS_IIA

NOTE: This rule also applies to invasive devices contacting injured mucous membrane
```

---

## INVASIVE DEVICE RULES (5-8)

### RULE 5: Invasive Body Orifice Devices
```
IF device_type == INVASIVE_BODY_ORIFICE
   AND NOT surgically_invasive:
   
   # First check connection to active devices
   IF connected_to_device_class IN [CLASS_IIA, CLASS_IIB, CLASS_III]:
      RETURN CLASS_IIA
   
   ELIF connected_to_device_class == CLASS_I OR no_active_connection:
      
      IF duration == TRANSIENT:
         RETURN CLASS_I
      
      ELIF duration == SHORT_TERM:
         IF location IN [ORAL_PHARYNX, EAR_CANAL, NASAL_CAVITY]:
            RETURN CLASS_I
         ELSE:
            RETURN CLASS_IIA
      
      ELIF duration == LONG_TERM:
         IF location IN [ORAL_PHARYNX, EAR_CANAL, NASAL_CAVITY]
            AND NOT absorbed_by_mucous_membrane:
            RETURN CLASS_IIA
         ELSE:
            RETURN CLASS_IIB
```

### RULE 6: Surgically Invasive Transient Devices
```
IF device_type == SURGICALLY_INVASIVE
   AND duration == TRANSIENT:
   
   # Check exceptions first (highest to lowest risk)
   IF (controls OR diagnoses OR monitors OR corrects) 
      AND defect_location IN [HEART, CENTRAL_CIRCULATORY]
      AND contact_type == direct:
      RETURN CLASS_III
   
   ELIF contact_location IN [HEART, CENTRAL_CIRCULATORY, CENTRAL_NERVOUS]
      AND contact_type == direct:
      RETURN CLASS_III
   
   ELIF device_type == reusable_surgical_instrument:
      RETURN CLASS_I
   
   ELIF supplies_energy_type == ionizing_radiation:
      RETURN CLASS_IIB
   
   ELIF has_biological_effect OR is_absorbed == [wholly, mainly]:
      RETURN CLASS_IIB
   
   ELIF administers_medicinal_products
      AND administration_method == delivery_system
      AND hazard_level == potentially_hazardous:
      RETURN CLASS_IIB
   
   ELSE:
      RETURN CLASS_IIA
```

### RULE 7: Surgically Invasive Short-Term Devices
```
IF device_type == SURGICALLY_INVASIVE
   AND duration == SHORT_TERM:
   
   # Check exceptions first (highest to lowest risk)
   IF (controls OR diagnoses OR monitors OR corrects)
      AND defect_location IN [HEART, CENTRAL_CIRCULATORY]
      AND contact_type == direct:
      RETURN CLASS_III
   
   ELIF contact_location IN [HEART, CENTRAL_CIRCULATORY, CENTRAL_NERVOUS]
      AND contact_type == direct:
      RETURN CLASS_III
   
   ELIF has_biological_effect OR is_absorbed IN [wholly, mainly]:
      RETURN CLASS_III
   
   ELIF supplies_energy_type == ionizing_radiation:
      RETURN CLASS_IIB
   
   ELIF undergoes_chemical_change_in_body:
      IF placement_location == TEETH:
         RETURN CLASS_IIA
      ELSE:
         RETURN CLASS_IIB
   
   ELIF administers_medicines:
      RETURN CLASS_IIB
   
   ELSE:
      RETURN CLASS_IIA
```

### RULE 8: Implantable and Long-Term Surgically Invasive Devices
```
IF device_type IN [IMPLANTABLE, SURGICALLY_INVASIVE]
   AND duration == LONG_TERM:
   
   # Check Class III exceptions first
   IF contact_location IN [HEART, CENTRAL_CIRCULATORY, CENTRAL_NERVOUS]
      AND contact_type == direct:
      RETURN CLASS_III
   
   ELIF has_biological_effect OR is_absorbed IN [wholly, mainly]:
      RETURN CLASS_III
   
   ELIF undergoes_chemical_change_in_body:
      IF placement_location == TEETH:
         RETURN CLASS_IIA
      ELSE:
         RETURN CLASS_III
   
   ELIF administers_medicinal_products:
      RETURN CLASS_III
   
   ELIF device_type IN [active_implantable_device, active_implantable_accessory]:
      RETURN CLASS_III
   
   ELIF device_subtype IN [breast_implant, surgical_mesh]:
      RETURN CLASS_III
   
   ELIF device_subtype == joint_replacement AND replacement_type IN [total, partial]:
      IF component_type IN [screw, wedge, plate, instrument]:
         RETURN CLASS_IIB  # Default for this rule
      ELSE:
         RETURN CLASS_III
   
   ELIF device_subtype IN [spinal_disc_replacement, spinal_column_contact]:
      IF component_type IN [screw, wedge, plate, instrument]:
         RETURN CLASS_IIB  # Default for this rule
      ELSE:
         RETURN CLASS_III
   
   ELIF placement_location == TEETH:
      RETURN CLASS_IIA
   
   ELSE:
      RETURN CLASS_IIB
```

---

## ACTIVE DEVICE RULES (9-13)

### RULE 9: Active Therapeutic Devices
```
IF device_type == ACTIVE
   AND device_category == therapeutic
   AND (administers_energy OR exchanges_energy):
   
   IF energy_characteristics == potentially_hazardous
      CONSIDERING [nature, density, site_of_application]:
      RETURN CLASS_IIB
   ELSE:
      RETURN CLASS_IIA

IF device_type == ACTIVE
   AND (controls OR monitors) performance_of == CLASS_IIB_therapeutic_device:
   RETURN CLASS_IIB

IF device_type == ACTIVE
   AND directly_influences performance_of == CLASS_IIB_therapeutic_device:
   RETURN CLASS_IIB

IF device_type == ACTIVE
   AND emits == ionizing_radiation
   AND purpose == therapeutic:
   RETURN CLASS_IIB

IF device_type == ACTIVE
   AND (controls OR monitors OR directly_influences) == active_implantable_device:
   RETURN CLASS_III
```

### RULE 10: Active Diagnostic and Monitoring Devices
```
IF device_type == ACTIVE
   AND purpose IN [diagnosis, monitoring]:
   
   # Check Class IIb conditions first
   IF monitors == vital_physiological_parameters
      AND variation_nature == immediate_danger_potential:
      RETURN CLASS_IIB
   
   ELIF diagnosis_context == patient_in_immediate_danger:
      RETURN CLASS_IIB
   
   ELIF emits == ionizing_radiation
      AND purpose IN [diagnostic_radiology, therapeutic_radiology, interventional_radiology]:
      RETURN CLASS_IIB
   
   ELIF controls OR monitors == ionizing_radiation_device:
      RETURN CLASS_IIB
   
   ELIF directly_influences == ionizing_radiation_device:
      RETURN CLASS_IIB
   
   # Check Class IIa conditions
   ELIF supplies_energy AND absorbed_by == human_body:
      IF purpose == illumination AND spectrum == visible:
         RETURN CLASS_I
      ELSE:
         RETURN CLASS_IIA
   
   ELIF images == in_vivo_radiopharmaceutical_distribution:
      RETURN CLASS_IIA
   
   ELIF allows_direct == diagnosis_or_monitoring
      AND monitors == vital_physiological_processes:
      RETURN CLASS_IIA
   
   ELSE:
      RETURN CLASS_I
```

### RULE 11: Software Devices
```
IF device_type == SOFTWARE:
   
   # Check Class III conditions first
   IF provides_information_for == [diagnosis, therapeutic_decisions]
      AND decision_impact == death OR decision_impact == irreversible_deterioration:
      RETURN CLASS_III
   
   # Check Class IIb conditions
   ELIF provides_information_for == [diagnosis, therapeutic_decisions]
      AND (decision_impact == serious_deterioration OR decision_impact == surgical_intervention):
      RETURN CLASS_IIB
   
   # Check Class IIa conditions
   ELIF provides_information_for == [diagnosis, therapeutic_decisions]:
      RETURN CLASS_IIA
   
   ELIF monitors == physiological_processes:
      IF monitors == vital_physiological_parameters
         AND variation_nature == immediate_danger_potential:
         RETURN CLASS_IIB
      ELSE:
         RETURN CLASS_IIA
   
   ELSE:
      RETURN CLASS_I
```

### RULE 12: Active Administration/Removal Devices
```
IF device_type == ACTIVE
   AND (administers OR removes) ANY OF [medicinal_products, body_liquids, substances]
   AND direction IN [to_body, from_body]:
   
   IF administration_manner == potentially_hazardous
      CONSIDERING [substance_nature, body_part, mode_of_application]:
      RETURN CLASS_IIB
   ELSE:
      RETURN CLASS_IIA
```

### RULE 13: Other Active Devices
```
IF device_type == ACTIVE
   AND no_other_active_rules_apply:
   RETURN CLASS_I
```

---

## SPECIAL RULES (14-22)

### RULE 14: Devices with Integral Medicinal Substance
```
IF incorporates_as_integral_part == medicinal_substance
   AND substance_can_be_used_separately == True
   AND substance_action == ancillary_to_device:
   RETURN CLASS_III

NOTE: Medicinal substance includes human blood or plasma derivatives
```

### RULE 15: Contraceptive and STD Prevention Devices
```
IF device_purpose IN [contraception, std_prevention]:
   
   IF device_type IN [IMPLANTABLE, long_term_invasive]:
      RETURN CLASS_III
   ELSE:
      RETURN CLASS_IIB
```

### RULE 16: Disinfecting, Cleaning, and Sterilizing Devices
```
# For contact lens products
IF device_purpose IN [disinfecting, cleaning, rinsing, hydrating]
   AND target == contact_lenses:
   RETURN CLASS_IIB

# For medical device disinfection/sterilization
IF device_purpose IN [disinfecting, sterilizing]
   AND target == medical_devices:
   
   IF device_type IN [disinfecting_solution, washer_disinfector]
      AND target_device_type == invasive
      AND process_stage == end_point:
      RETURN CLASS_IIB
   ELSE:
      RETURN CLASS_IIA

# Exception for physical cleaning only
IF device_purpose == cleaning
   AND target != contact_lenses
   AND method == physical_action_only:
   RETURN (apply_other_rules)  # This rule does not apply
```

### RULE 17: X-Ray Diagnostic Imaging Devices
```
IF device_purpose == recording_diagnostic_images
   AND image_source == x_ray_radiation:
   RETURN CLASS_IIA
```

### RULE 18: Devices with Biological Tissues/Cells
```
IF manufactured_with IN [human_tissue, human_cells, animal_tissue, animal_cells]
   OR manufactured_with IN [human_derivatives, animal_derivatives]
   AND viability IN [non_viable, rendered_non_viable]:
   
   IF source_type == animal
      AND contact == intact_skin_only:
      RETURN (apply_other_rules)  # Exception - use other rules
   ELSE:
      RETURN CLASS_III
```

### RULE 19: Nanomaterial Devices
```
IF incorporates == nanomaterial OR consists_of == nanomaterial:
   
   IF internal_exposure_potential == [high, medium]:
      RETURN CLASS_III
   
   ELIF internal_exposure_potential == low:
      RETURN CLASS_IIB
   
   ELIF internal_exposure_potential == negligible:
      RETURN CLASS_IIA
```

### RULE 20: Inhalation Medicinal Product Devices
```
IF device_type == INVASIVE_BODY_ORIFICE
   AND NOT surgically_invasive
   AND administers == medicinal_products
   AND administration_route == inhalation:
   
   IF mode_of_action == essential_impact_on_drug_efficacy_or_safety:
      RETURN CLASS_IIB
   
   ELIF treats == life_threatening_conditions:
      RETURN CLASS_IIB
   
   ELSE:
      RETURN CLASS_IIA
```

### RULE 21: Absorbable Substance Devices
```
IF device_composition == [substances, substance_combinations]
   AND (introduced_via == body_orifice OR applied_to == skin)
   AND (absorbed_by == human_body OR locally_dispersed == True):
   
   IF systemically_absorbed == True
      AND purpose == achieve_intended_purpose:
      RETURN CLASS_III
   
   ELIF location IN [stomach, lower_gastrointestinal_tract]
      AND systemically_absorbed == True
      AND (device_absorbed OR metabolism_products_absorbed):
      RETURN CLASS_III
   
   ELIF applied_to IN [skin, nasal_cavity, oral_cavity_to_pharynx]
      AND achieves_purpose_on == application_site:
      RETURN CLASS_IIA
   
   ELSE:
      RETURN CLASS_IIB
```

### RULE 22: Active Therapeutic with Integrated Diagnostic
```
IF device_type == ACTIVE
   AND device_category == therapeutic
   AND has_integrated == diagnostic_function
   AND diagnostic_significantly_determines == patient_management
   AND system_type IN [closed_loop, automated_external_defibrillator]:
   RETURN CLASS_III
```

---

## IMPLEMENTATION NOTES

### Priority and Conflict Resolution
1. If multiple rules apply, use the rule that gives the HIGHEST classification
2. Special rules (14-22) take precedence over general rules (1-13)
3. Specific exceptions within a rule override the default classification

### Boolean Logic Operators
- **AND**: All conditions must be true
- **OR**: At least one condition must be true
- **IN**: Value must be in the specified list
- **ANY OF**: At least one item from list applies
- **CONSIDERING**: Evaluate these factors in determination

### Input Requirements for Classification Function
```python
Required device attributes:
- device_type: str  # NON_INVASIVE, INVASIVE_BODY_ORIFICE, SURGICALLY_INVASIVE, IMPLANTABLE, ACTIVE, SOFTWARE
- duration: str  # TRANSIENT, SHORT_TERM, LONG_TERM (if applicable)
- contact_location: list  # Body parts contacted
- purpose: str  # Primary function
- device_properties: dict  # Additional characteristics
- connections: dict  # Connected devices and their classes
```

### Output Format
```python
Return type: dict
{
    "classification": str,  # CLASS_I, CLASS_IIA, CLASS_IIB, CLASS_III
    "applicable_rules": list,  # Rule numbers that applied
    "reasoning": str  # Brief explanation
}
```
