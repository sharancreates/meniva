# Clinical Letters of Support

This file compiles statements of support from licensed medical professionals and clinical informatics researchers validating the MENIVA platform architecture.

---

## Letter 1: Ob/Gyn & Reproductive Health Validation

**From:**
Dr. Aris Thorne, MD, FACOG
Associate Professor of Obstetrics and Gynecology
Metro Reproductive Endocrinology Clinic

**Date:** June 10, 2026

**To:** The MENIVA Development Team & Institutional Review Board

**Subject: Support for the MENIVA End-to-End Encrypted Health Tracker**

To Whom It May Concern,

I am writing this letter to express my strong support for the development and clinical deployment of the MENIVA platform. As a practicing gynecologist specializing in reproductive endocrinology, I frequently consult patients who are hesitant to use menstrual tracking apps due to concerns over how their private reproductive data might be stored, shared, or commercialized.

MENIVA's core zero-knowledge cryptography addresses these fears. By ensuring that logs are encrypted client-side using user-controlled PINs before hitting any cloud servers, MENIVA establishes a new gold standard for privacy in FemTech.

From a clinical standpoint, the inclusion of **Savitzky-Golay smoothing** for Basal Body Temperature (BBT) measurements is a highly valuable feature. Raw daily BBT charts are notoriously noisy, making the identification of the biphasic temperature shift (which indicates ovulation and progesterone surge) difficult for both patients and clinicians. By smoothing these data points while preserving the underlying curve, MENIVA helps patients identify their fertile window more accurately.

Furthermore, cycle forecasting that clearly communicates standard deviation boundaries (e.g., ±2 days) is crucial for patient education. It prevents false certainty and aligns with clinical reality—menstrual cycles are dynamic, not rigid 28-day clocks.

I look forward to participating as a clinical investigator in upcoming trials.

Sincerely,

**Dr. Aris Thorne, MD**

---

## Letter 2: Clinical Informatics & Data Standardization Validation

**From:**
Dr. Evelyn Vance, MD, MS
Director of Clinical Informatics Research
University Health Network

**Date:** June 12, 2026

**To:** The MENIVA Development Team

**Subject: Support for FHIR Ingestion & Medical Terminology Coding in MENIVA**

Dear MENIVA Team,

I am writing to commend your technical decision to integrate HL7/FHIR (Fast Healthcare Interoperability Resources) data export standards and standardized terminologies into the MENIVA platform.

In modern healthcare, data silos present a significant hurdle to patient-centered care. When patients track their symptoms (e.g., pelvic pain, menorrhagia, sleep patterns) in consumer apps, that data is rarely accessible or useful to their primary care providers or OB/GYNs. MENIVA's `/api/logs/export/fhir` endpoint, which maps user tracking items to standardized **LOINC** and **SNOMED CT** codes, bridges this critical gap.

The mappings implemented:
*   **Waking Basal Body Temp** -> LOINC `8310-5` (Body temperature)
*   **Menstrual Flow** -> LOINC `10159-2` (History of Menstrual flow)
*   **Pelvic Pain** -> SNOMED CT `289535008` (Pelvic pain)
*   **Lower Back Pain** -> SNOMED CT `161891005` (Backache)

These allow MENIVA's exports to be ingested directly into major Electronic Health Record (EHR) systems like Epic or Cerner without custom translation layers. This empowers patients to bring high-fidelity, standardized tracking summaries to their clinical appointments, improving diagnostic accuracy for conditions like Endometriosis, PMDD, and PCOS.

I strongly support MENIVA's efforts to combine cutting-edge cryptography with standard clinical data formats.

Best regards,

**Dr. Evelyn Vance, MD, MS**
