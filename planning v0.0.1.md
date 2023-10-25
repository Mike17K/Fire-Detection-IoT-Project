2 ενδιαμεσες παρουσιασεις

1η τελος οκτομβρη 30/10 - 3/11
παρουσιαση buissness "pich"

- problem description
- solution proposal (pros)
- unique value proposition (γιατι το κανεις αυτο και τι διαφορετικο ειναι απο την αγορα)
- target group
- draft website
- kit hardware and pricing (cost total, installation cost, maintaining cost)

2η τελη νοεμβη
παρουσιαση alpha version (δουλευουν τμηματα της εφαρμογης)

- αναγκες
- αρχητεκτονικη συστηαματος
  (database : fiware)
- βηματα υλοποιησης - χρονοδιαγραμμα
- overview απο τα τμηματα της εφαρμογης να δειξουμε πως δουλευει το API

Naroband IoT ?
LoRa
zigbi

ideas:
θερμοκρασιομετρα μπολικα ανα 200 μετρα σε βουνο για να παρακολουθησομε την διαφορα θερμοκρασιων

καμερα με ΑΙ για φωτιες

# Βηματα

## ερευνα για το πως γινεται η ανιχνευση πυρκαγιων

**Video Cameras and Imaging:**

- Video cameras sensitive to visible light spectrum are used for daytime fire and smoke detection.
- Infrared (IR) thermal imaging cameras detect heat flow from fires, working effectively day and night.
- Black and white, color frequency, and IR cameras are integrated into systems like AlarmEYE and EYEfi SPARC for comprehensive detection.

**Atmospheric Analysis:**

- The Forest Fire Finder employs intelligent analysis of atmospheric light absorption to distinguish between organic forest smoke and industrial emissions based on the atmosphere's chemical composition.
- Techniques such as IR spectrometers are used to identify spectral characteristics of smoke.

**Optical Camera Systems:**

- Systems like ForestWatch and FireHawk utilize tower-mounted optical camera sensors for detecting smoke during the day and fire glow at night.
- ForestWatch's optical sensors rotate at specific intervals, providing continuous monitoring.

**Wireless Sensor Networks:**

- Researchers propose using mesh networks of sensors integrated with IP cameras for forest fire detection.
- These sensor networks can trigger alarms and activate nearby cameras to capture real-time fire images.
- Clustering and routing protocols, like MCF, are used to relay data to central nodes for analysis and reporting.

**GPS and Radio Wave Sensors:**

- Conard et al. proposed a system where GPS handheld devices and radio wave sensors transmit signals to GPS satellites to pinpoint fire locations.
- Unique identity codes are sent to the central monitoring database to display the fire's location on a map.

**Data Fusion and Algorithms:**

- Complex systems like FIRESENSE integrate multiple sensors, optical cameras, IR cameras, PTZ cameras, and weather stations.
- Data fusion algorithms are applied to provide a comprehensive understanding of fire events and improve decision-making.
- These systems aim to produce reports, graphs, and curves to assist firefighters.

**Challenges and Limitations:**

- Current systems may have limitations in accurately localizing fires due to factors such as topography and the potential for false alarms, influenced by daily sun movement, clouds, atmospheric changes, and vegetation.

## ερευνα για LoRa και Zigby και συσκευες ετοιμες λυσεις

- 100 m αυτονομια το καθε ενα και λιγο λιγοτερο σε δασος λογω εμποδιων
- LoRa 10 - 20 Km

# solutions

- grid 50 x 50 metra
- zigbee
- πανω σε κλαδια
- εφαρμογη με gps για τοποθεση
- zigbee, temperature, smoke
- waterproff in a jar can
- camera AI sto gateway
- gateway - weather station

# Senario
the sensors will send data only when requested or when the values rise above a certain level
the weather station along with the temperature sensors of the ground will create a prediction of danger level
above a certain danger level the system will go into high alert (sensors will gather data more frequently)
if the temperature and smoke sensor detect a rise above a warning threshhold they will gather data at a faster pace
if they rise above a danger threshold they will signal a possible fire to the gateway

# Pros
- cost benefit - long time support
- fast responce
