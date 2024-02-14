# Πρώτη παρουσίαση

## Περιγραφή προβλήματος

Κάθε χρόνο στην Ελλάδα παρατηρούμε φαινόμενα πυρκαγιών σε δασικές περιοχές, με αποτέλεσμα να
καταστρέφονται μεγάλες εκτάσεις πρασίνου. Τον τελευταίο χρόνο έχουν καεί περίπου 1.8 εκατομμύρια
στρέμματα δασικής έκτασης σε όλη την Ελλάδα.

Ο σκοπός αυτού του πρότζεκτ είναι η σχεδίαση ενός συστήματος για την πρόβλεψη επικινδυνότητας
πυρκαγίας σε μια περιοχή και κυρίως την έγκαιρη ανίχνευση ενεργών εστιών πυρκαγίας σε όσο το
δυνατό μικρότερο χρόνο από την ώρα εκδήλωσης τους, έτσι ώστε να κινητοποιηθούν άμεσα οι μηχανισμοί
πυρόσβεσης.

## Γενική μεθοδολογία επίλυσης

Η λύση που προτείνουμε περιλαμβάνει τα εξής βασικά δομικά στοιχεία

- Αισθητήρες θα τοποθετούνται πάνω σε δέντρα (θα ανιχνεύουν θερμοκρασία, καπνό, υγρασία)
    σε τακτά σημεία έτσι ώστε να καλύπτουν πυκνά την περιοχή στην οποία θα γίνει η ανίχνευση.
    Οι αισθητήρες αυτοί θα χρησιμεύουν στην ανίχνευση ενεργών εστιών πυρκαγιάς αφού όταν υπάρχει
    φωτιά η θερμοκρασία αυξάνεται, η υγρασία μειώνεται και παράγεται αρκετός καπνός.

- Οι αισθητήρες αυτοί θα επικοινωνούν με το υπόλοιπο σύστημα μέσω τεχνολογίας LoRa σε gateway
    τοποθετημένα εντός της περιοχής. Μαζί με τη συνδεσιμότητα το gateway θα περιλαμβάνει
    αισθητήρα ταχύτητας ανέμου, ο οποίος θα χρησιμεύει για την δημιουργία εκτίμησης
    επικινδυνότητας. Επίσης θα φέρει κάμερα ώστε να μπορεί να πραγματοποιήθει οπτική
    επιβεβαίωση του συμβάντος και να αντλήθουν παραπάνω πληροφορίες για την τοποθεσία
    και την έκταση της πυρκαγιάς.

- Το gateway θα συνδέεται με σήμα κινητής στο internet (μελλοντικά θα μπορούσε και με δορυφόρο),
    ώστε οι πληφορίες να είναι διαθέσιμες από
    οπουδήποτε για ανάλυση και μελέτη. Η επεξεργασία των δεδομένων θα γίνεται σε απομακρυσμένο
    server (cloud computing), που θα έχει κατάλληλη επεξεργαστική ισχή για να τρέξει τα μοντέλα
    τεχνητής νοημοσύνης που θα παράγουν την πρόβλεψη επικινδυνότητας και την τελική εκτίμηση
    για πυρκαγία εντός της περιοχής.

- Το σύστημα θα παρέχει μια διεπαφή για προβολή της τωρινής κατάστασης του συστήματος και θα
    ειδοποιεί σε περιπτώσεις ανάγκης.

## Ιδανική λειτουργία συστήματος

### Εγκατάσταση συστήματος

Στην περιοχή που θα γίνει η εγκατάσταση του συστήματος, θα τοποθετηθούν οι αισθητήρες πάνω στα
δέντρα με ομοιόμορφη και πυκνή κατανομή, έτσι ώστε να υπάρχει πλήρη κάλυψη με το ελάχιστο δυνατό
κόστος και θα τοποθετηθούν μερικά gateway σε στρατηγικά σημεία προκειμένου κάθε ένα να έχει τη
μέγιστη δυνατή οπτική εμβέλεια.

Κατά τη διάρκεια της εγκατάστασης θα καταγράφεται η τοποθεσία του κάθε αισθητήρα, μέσω εφαρμογής
στο κινητό του τεχνικού.

### Ανίχνευση πυρκαγίας

Κάθε αισθητήρας θα στέλνει ανά τακτά χρονικά διαστήματα στο gateway στο οποίο αντιστοιχεί
τις τιμές που καταγράφει

Σε καιρούς επικινδυνότητας το σύστημα θα μπαίνει σε επιφυλακή, δηλάδη οι αισθητήρες θα καταγράφουν
δεδομένα με μεγαλύτερο ρυθμό. Επίσης θα τραβάει φωτογραφία μέσω της κάμερας προς την κατέυθυνση
που θεωρείται ότι υπάρχει η μεγαλύτερη επικινδυνότητα.

Το δεδομένα από όλους τους αιθητήρες θα συσωρεύονται και θα αναλύονται από κάποιο μοντέλο, έτσι
ώστε να αποφευχθούν περιπτώσεις false positive και να εξασφαλίζεται μεγαλύτερη ακρίβεια πρόβλεψης.

### Ειδοποίηση χειρηστή & επιβεβαίωση

Όταν το σύστημα θεωρήσει ότι υπάρχει πυρκαγία σε μια περιοχή, τότε θα ειδοποιήται ο χειρηστής του
συστήματος, έτσι ώστε να επιβεβαιώσει το συμβάν μέσω των καμερών που θα υπάρχουν στην περιοχή και
θα κινητοποιεί άμεσα τις κατάλληλες αρχές.

## Interface Mockup
TODO

## Απαραίτητο υλικό

### Αισθητήρες πάνω στα δέντρα
- Αισθητήρας θερμοκρασίας
- Αισθητήρας καπνού
- Αισθητήρας υγρασίας
- Κεραία Lora
- Microcontroller (Arduino?)
- Μπαταρία
- Προστασία από το περιβάλλον

Για του σκοπούς του project θα χρησιμοποιήσουμε τον τάδε

### Gateway
- Αισθητήρας ταχύτητας ανέμου
- Κάμερα με δυνατότητα προσανατολισμού
- Κεραία LoRa
- Κεραία κινητής
- Microcontroller? (RasberryPi?) (για AI)
- Μεγάλες Μπαταρίες
- Φωτοβολταικό?
- Προστασία από το περιβάλλον

## Υπάρχοντα σύστηματα & διαφοροποιήσεις

### SILVANUS project

!(./CTL_IoT.png)

Το SILVANUS project προτείνει μια παρόμοια συσκευή που θα τοποθετήται πάνω σε δέντρα η οποία ομώς
είναι αρκετά πιο περίπλοκη στη λειτουργία της καθώς εκτελεί το υπολογιστικό κομμάτι της ανίχνευσης
πάνω στη συσκευή, γεγονός που απαιτεί παραπάνω κατανάλωση ισχύος και εν τέλει αυξάνει το κόστος
σημαντικά. Η δικία μας πρόταση λόγω της απλότητας της υλοποίησης εξασφαλίζει χαμηλό κόστος
παραγωγής και χαμηλή κατανάλωση ενέργειας, άρα μεγαλύτερη διάρκεια ζωής της συσκευής και κατά
συνέπεια μειώνει το κόστος συντήρησης.

Επίσης κομμάτι του SILVANUS project είναι η ανίχνευση πυρκαγίας μέσω drone τα οποία πρέπει να
βρίσκονται σε διαρκή πτήση πάνω από την προστατευόμενη περιοχή. Η λύση αυτή όμως προϋποθέτει
την υπάρξη προσωπικού που να χειρίζεται το σύστημα σε 24ωρη βάση 7 μέρες την εβδομάδα, το οποίο
αυξάνει σημαντικά το κόστος λειτουργίας.

### ALERTCalifornia

ALERTCalifornia has more than 1,000 high-definition, pan-tilt-zoom cameras deployed across California, providing a 24-hour backcountry network with near-infrared night vision to monitor disasters such as active wildfires. ALERTCalifornia cameras can perform 360-degree sweeps approximately every two minutes and can view as far as 60 miles on a clear day and 120 miles on a clear night. Explore our “camera quilt” to view live camera feeds and for more details on camera and network status.

Με ένα σύστημα που αποτελείται αποκλειστικά από κάμερες δεν είναι δυνατή η πλήρη κάλυψη μιας
περιοχής με χαμηλό σχετικά κόστος, αφού πάντα θα υπάρχουν σημεία στα οποία δεν θα υπάρχει οπτική
επαφή. Επιπλέον οι κάμερες έχουν περιορισμένη ανάλυση και κακή απόδοση κατά τη διάρκεια της νύχτας
οπότε δεν είναι σίγουρο ότι μπορούν να εντοπίσουν εστία φωτιάς όταν αυτή βρίσκεται σε μεγάλη
απόσταση.

## Case Study

Θα εξετάσουμε την υλοποίηση του συστήματος στη δασική περιοχή
!(./case study map.png)