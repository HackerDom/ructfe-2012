#!/usr/bin/env python

import random
import time
import md5
import hashlib
import re
import errno
import socket
import sys

from M2Crypto.RSA import *

HOST = sys.argv[1]
PORT = 2012

TIMEOUT = 4

# exit codes
OK = 101
NOFLAG = 102
MUMBLE = 103
NOCONNECT = 104
INTERNALERROR = 110

cities = [
     "ATL", "LHR", "PEK", "ORD", "HND", "CDG", "LAX", "DFW", "FRA", "DEN",
     "MAD", "JFK", "HKG", "AMS", "DXB"
]

airlines = [ "DL", "UA", "WN", "AA", "LH", "CZ", "FR", "AF", "MU", "US" ]

classes = ["F", "A", "P", "J", "C", "D", "Y", "S", "M", "K", "V", "T", "Q",
           "W", "G", "L", "X", "H", "U", "N", "B", "T", "Z"]

names = [
    "JACOB", "MASON", "WILLIAM", "JAYDEN", "NOAH", "MICHAEL", "ETHAN",
    "ALEXANDER", "AIDEN", "DANIEL", "ANTHONY", "MATTHEW", "ELIJAH",
    "JOSHUA", "LIAM", "ANDREW", "JAMES", "DAVID", "BENJAMIN",
    "LOGAN", "CHRISTOPHER", "JOSEPH", "JACKSON", "GABRIEL", "RYAN",
    "SAMUEL", "JOHN", "NATHAN", "LUCAS", "CHRISTIAN", "JONATHAN",
    "CALEB", "DYLAN", "LANDON", "ISAAC", "GAVIN", "BRAYDEN",
    "TYLER", "LUKE", "EVAN", "CARTER", "NICHOLAS", "ISAIAH",
    "OWEN", "JACK", "JORDAN", "BRANDON", "WYATT", "JULIAN",
    "AARON", "JEREMIAH", "ANGEL", "CAMERON", "CONNOR", "HUNTER",
    "ADRIAN", "HENRY", "ELI", "JUSTIN", "AUSTIN", "ROBERT",
    "CHARLES", "THOMAS", "ZACHARY", "JOSE", "LEVI", "KEVIN",
    "SEBASTIAN", "CHASE", "AYDEN", "JASON", "IAN", "BLAKE",
    "COLTON", "BENTLEY", "DOMINIC", "XAVIER", "OLIVER", "PARKER",
    "JOSIAH", "ADAM", "COOPER", "BRODY", "NATHANIEL", "CARSON",
    "JAXON", "TRISTAN", "LUIS", "JUAN", "HAYDEN", "CARLOS",
    "JESUS", "NOLAN", "COLE", "ALEX", "MAX", "GRAYSON",
    "BRYSON", "DIEGO", "JADEN", "VINCENT", "EASTON", "ERIC",
    "MICAH", "KAYDEN", "JACE", "AIDAN", "RYDER", "ASHTON",
    "BRYAN", "RILEY", "HUDSON", "ASHER", "BRYCE", "MILES",
    "KALEB", "GIOVANNI", "ANTONIO", "KADEN", "COLIN", "KYLE",
    "BRIAN", "TIMOTHY", "STEVEN", "SEAN", "MIGUEL", "RICHARD",
    "IVAN", "JAKE", "ALEJANDRO", "SANTIAGO", "AXEL", "JOEL",
    "MAXWELL", "BRADY", "CADEN", "PRESTON", "DAMIAN", "ELIAS",
    "JAXSON", "JESSE", "VICTOR", "PATRICK", "JONAH", "MARCUS",
    "RYLAN", "EMMANUEL", "EDWARD", "LEONARDO", "CAYDEN", "GRANT",
    "JEREMY", "BRAXTON", "GAGE", "JUDE", "WESLEY", "DEVIN",
    "ROMAN", "MARK", "CAMDEN", "KAIDEN", "OSCAR", "ALAN",
    "MALACHI", "GEORGE", "PEYTON", "LEO", "NICOLAS", "MADDOX",
    "KENNETH", "MATEO", "SAWYER", "COLLIN", "CONNER", "CODY",
    "ANDRES", "DECLAN", "LINCOLN", "BRADLEY", "TREVOR", "DEREK",
    "TANNER", "SILAS", "EDUARDO", "SETH", "JAIDEN", "PAUL",
    "JORGE", "CRISTIAN", "GARRETT", "TRAVIS", "ABRAHAM", "OMAR",
    "JAVIER", "EZEKIEL", "TUCKER", "HARRISON", "PETER", "DAMIEN",
    "GREYSON", "AVERY", "KAI", "WESTON", "EZRA", "XANDER",
    "JAYLEN", "CORBIN", "FERNANDO", "CALVIN", "JAMESON", "FRANCISCO",
    "MAXIMUS", "JOSUE", "RICARDO", "SHANE", "TRENTON", "CESAR",
    "CHANCE", "DRAKE", "ZANE", "ISRAEL", "EMMETT", "JAYCE",
    "MARIO", "LANDEN", "KINGSTON", "SPENCER", "GRIFFIN", "STEPHEN",
    "MANUEL", "THEODORE", "ERICK", "BRAYLON", "RAYMOND", "EDWIN",
    "CHARLIE", "ABEL", "MYLES", "BENNETT", "JOHNATHAN", "ANDRE",
    "ALEXIS", "EDGAR", "TROY", "ZION", "JEFFREY", "HECTOR",
    "SHAWN", "LUKAS", "AMIR", "TYSON", "KEEGAN", "KYLER",
    "DONOVAN", "GRAHAM", "SIMON", "EVERETT", "CLAYTON", "BRADEN",
    "LUCA", "EMANUEL", "MARTIN", "BRENDAN", "CASH", "ZANDER",
    "JARED", "RYKER", "DANTE", "DOMINICK", "LANE", "KAMERON",
    "ELLIOT", "PAXTON", "RAFAEL", "ANDY", "DALTON", "ERIK",
    "SERGIO", "GREGORY", "MARCO", "EMILIANO", "JASPER", "JOHNNY",
    "DEAN", "DREW", "CAIDEN", "SKYLER", "JUDAH", "MAXIMILIANO",
    "ADEN", "FABIAN", "ZAYDEN", "BRENNAN", "ANDERSON", "ROBERTO",
    "REID", "QUINN", "ANGELO", "HOLDEN", "CRUZ", "DERRICK",
    "GRADY", "EMILIO", "FINN", "ELLIOTT", "PEDRO", "AMARI",
    "FRANK", "ROWAN", "LORENZO", "FELIX", "COREY", "DAKOTA",
    "COLBY", "BRAYLEN", "DAWSON", "BRYCEN", "ALLEN", "JAX",
    "BRANTLEY", "TY", "MALIK", "RUBEN", "TREY", "BROCK",
    "COLT", "DALLAS", "JOAQUIN", "LELAND", "BECKETT", "JETT",
    "LOUIS", "GUNNER", "ADAN", "JAKOB", "COHEN", "TAYLOR",
    "ARTHUR", "MARCOS", "MARSHALL", "RONALD", "JULIUS", "ARMANDO",
    "KELLEN", "DILLON", "BROOKS", "CADE", "DANNY", "NEHEMIAH",
    "BEAU", "JAYSON", "DEVON", "TRISTEN", "ENRIQUE", "RANDY",
    "GERARDO", "PABLO", "DESMOND", "RAUL", "ROMEO", "MILO",
    "JULIO", "KELLAN", "KARSON", "TITUS", "KEATON", "KEITH",
    "REED", "ALI", "BRAYDON", "DUSTIN", "SCOTT", "TRENT",
    "WAYLON", "WALTER", "DONALD", "ISMAEL", "PHILLIP", "IKER",
    "ESTEBAN", "JAIME", "LANDYN", "DARIUS", "DEXTER", "MATTEO",
    "COLTEN", "EMERSON", "PHOENIX", "KING", "IZAIAH", "KARTER",
    "ALBERT", "JERRY", "TATE", "LARRY", "SAUL", "PAYTON",
    "AUGUST", "JALEN", "ENZO", "JAY", "ROCCO", "KOLTON",
    "RUSSELL", "LEON", "PHILIP", "GAEL", "QUENTIN", "TONY",
    "MATHEW", "KADE", "GIDEON", "DENNIS", "DAMON", "DARREN",
    "KASON", "WALKER", "JIMMY", "ALBERTO", "MITCHELL", "ALEC",
    "RODRIGO", "CASEY", "RIVER", "MAVERICK", "AMARE", "BRAYAN",
    "MOHAMED", "ISSAC", "YAHIR", "ARTURO", "MOISES", "MAXIMILIAN",
    "KNOX", "BARRETT", "DAVIS", "GUSTAVO", "CURTIS", "HUGO",
    "REECE", "CHANDLER", "MAURICIO", "JAMARI", "ABRAM", "URIEL",
    "BRYANT", "ARCHER", "KAMDEN", "SOLOMON", "PORTER", "ZACKARY",
    "ADRIEL", "RYLAND", "LAWRENCE", "NOEL", "ALIJAH", "RICKY",
    "RONAN", "LEONEL", "MAURICE", "CHRIS", "ATTICUS", "BRENDEN",
    "IBRAHIM", "ZACHARIAH", "KHALIL", "LANCE", "MARVIN", "DANE",
    "BRUCE", "CULLEN", "ORION", "NIKOLAS", "PIERCE", "KIERAN",
    "BRAEDEN", "KOBE", "FINNEGAN", "REMINGTON", "MUHAMMAD", "PRINCE",
    "ORLANDO", "ALFREDO", "MEKHI", "SAM", "RHYS", "JACOBY",
    "EDDIE", "ZAIDEN", "ERNESTO", "JOE", "KRISTOPHER", "JONAS",
    "GARY", "JAMISON", "NICO", "JOHAN", "GIOVANI", "MALCOLM",
    "ARMANI", "WARREN", "GUNNAR", "RAMON", "FRANKLIN", "KANE",
    "BYRON", "CASON", "BRETT", "ARI", "DEANDRE", "FINLEY",
    "JUSTICE", "DOUGLAS", "CYRUS", "GIANNI", "TALON", "CAMRON",
    "CANNON", "NASH", "DORIAN", "KENDRICK", "MOSES", "ARJUN",
    "SULLIVAN", "KASEN", "DOMINIK", "AHMED", "KORBIN", "ROGER",
    "ROYCE", "QUINTON", "SALVADOR", "ISAIAS", "SKYLAR", "RAIDEN",
    "TERRY", "BRODIE", "TOBIAS", "MORGAN", "FREDERICK", "MADDEN",
    "CONOR", "REESE", "BRAIDEN", "KELVIN", "JULIEN", "KRISTIAN",
    "RODNEY", "WADE", "DAVION", "NICKOLAS", "XZAVIER", "ALVIN",
    "ASA", "ALONZO", "EZEQUIEL", "BOSTON", "NASIR", "NELSON",
    "JASE", "LONDON", "MOHAMMED", "RHETT", "JERMAINE", "ROY",
    "MATIAS", "ACE", "CHAD", "MOSHE", "AARAV", "KEAGAN",
    "ALDO", "BLAINE", "MARC", "ROHAN", "BENTLY", "TRACE",
    "KAMARI", "LAYNE", "CARMELO", "DEMETRIUS", "LAWSON", "NATHANAEL",
    "URIAH", "TERRANCE", "AHMAD", "JAMARION", "SHAUN", "KALE",
    "NOE", "CARL", "JAYDON", "CALLEN", "MICHEAL", "JAXEN",
    "LUCIAN", "JAXTON", "RORY", "QUINCY", "GUILLERMO", "JAVON",
    "KIAN", "WILSON", "JEFFERY", "JOEY", "KENDALL", "HARPER",
    "JENSEN", "MOHAMMAD", "DAYTON", "BILLY", "JONATHON", "JADIEL",
    "WILLIE", "JADON", "CLARK", "REX", "FRANCIS", "KASH",
    "MALAKAI", "TERRELL", "MELVIN", "CRISTOPHER", "LAYTON", "ARIEL",
    "SYLAS", "GERALD", "KODY", "MESSIAH", "SEMAJ", "TRISTON",
    "BENTLEE", "LEWIS", "MARLON", "TOMAS", "AIDYN", "TOMMY",
    "ALESSANDRO", "ISIAH", "JAGGER", "NIKOLAI", "OMARI", "SINCERE",
    "CORY", "RENE", "TERRENCE", "HARLEY", "KYLAN", "LUCIANO",
    "ARON", "FELIPE", "REGINALD", "TRISTIAN", "URIJAH", "BECKHAM",
    "JORDYN", "KAYSON", "NEIL", "OSVALDO", "AYDIN", "ULISES",
    "DEACON", "GIOVANNY", "CASE", "DAXTON", "WILL", "LEE",
    "MAKAI", "RAPHAEL", "TRIPP", "KOLE", "CHANNING", "SANTINO",
    "STANLEY", "ALLAN", "ALONSO", "JAMAL", "JORDEN", "DAVIN",
    "SOREN", "ARYAN", "AYDAN", "CAMREN", "JASIAH", "RAY",
    "BEN", "JON", "BOBBY", "DARRELL", "MARKUS", "BRANDEN",
    "HANK", "MATHIAS", "ADONIS", "DARIAN", "JESSIE", "MARQUIS",
    "VICENTE", "ZAYNE", "KENNY", "RAYLAN", "JEFFERSON", "STEVE",
    "WAYNE", "LEONARD", "KOLBY", "AYAAN", "EMERY", "HARRY",
    "RASHAD", "ADRIEN", "DAX", "DWAYNE", "SAMIR", "ZECHARIAH",
    "YUSUF", "RONNIE", "TRISTIN", "BENSON", "MEMPHIS", "LAMAR",
    "MAXIM", "BOWEN", "ELLIS", "JAVION", "TATUM", "CLAY",
    "ALEXZANDER", "DRAVEN", "ODIN", "BRANSON", "ELISHA", "RUDY",
    "ZAIN", "RAYAN", "STERLING", "BRENNEN", "JAIRO", "BRENDON",
    "KAREEM", "RYLEE", "WINSTON", "JEROME", "KYSON", "LENNON",
    "LUKA", "CROSBY", "DESHAWN", "ROLAND", "ZAVIER", "CEDRIC",
    "VANCE", "NIKO", "GAUGE", "KAEDEN", "KILLIAN", "VINCENZO",
    "TEAGAN", "TREVON", "KYMANI", "VALENTINO", "ABDULLAH", "BO",
    "DARWIN", "HAMZA", "KOLTEN", "EDISON", "JOVANI", "AUGUSTUS",
    "GAVYN", "TOBY", "DAVIAN", "ROGELIO", "MATTHIAS", "BRENT",
    "HAYES", "BROGAN", "JAMIR", "DAMION", "EMMITT", "LANDRY",
    "CHAIM", "JAYLIN", "YOSEF", "KAMRON", "LIONEL", "VAN",
    "BRONSON", "CASEN", "JUNIOR", "MISAEL", "YANDEL", "ALFONSO",
    "GIANCARLO", "ROLANDO", "ABDIEL", "AADEN", "DEANGELO", "DUNCAN",
    "ISHAAN", "JAMIE", "MAXIMO", "CAEL", "CONRAD", "RONIN",
    "XAVI", "DOMINIQUE", "EAN", "TYRONE", "CHACE", "CRAIG",
    "MAYSON", "QUINTIN", "DERICK", "BRADYN", "IZAYAH", "ZACHERY",
    "WESTIN", "ALVARO", "JOHNATHON", "RAMIRO", "KONNER", "LENNOX",
    "MARCELO", "BLAZE", "EUGENE", "KEENAN", "BRUNO", "DEEGAN",
    "RAYDEN", "CALE", "CAMRYN", "EDEN", "JAMAR", "LEANDRO",
    "SAGE", "MARCEL", "JOVANNI", "RODOLFO", "SEAMUS", "CAIN",
    "DAMARION", "HAROLD", "JAEDEN", "KONNOR", "JAIR", "CALLUM",
    "ROWEN", "RYLEN", "ARNAV", "ERNEST", "GILBERTO", "IRVIN",
    "FISHER", "RANDALL", "HEATH", "JUSTUS", "LYRIC", "MASEN",
    "AMOS", "FRANKIE", "HARVEY", "KAMRYN", "ALDEN", "HASSAN",
    "SALVATORE", "THEO", "DARIEN", "GILBERT", "KRISH", "MIKE",
    "TODD", "JAIDYN", "ISAI", "SAMSON", "CASSIUS", "HEZEKIAH",
    "MAKHI", "ANTOINE", "DARNELL", "REMY", "STEFAN", "CAMDYN",
    "KYRON", "CALLAN", "DARIO", "JEDIDIAH", "LEONIDAS", "DEVEN",
    "FLETCHER", "SONNY", "REAGAN", "YADIEL", "JERIMIAH", "EFRAIN",
    "SIDNEY", "SANTOS", "ADITYA", "BRENTON", "BRYSEN", "NIXON",
    "TYRELL", "VAUGHN", "ELVIS", "FREDDY", "DEMARCUS", "GAIGE",
    "JAYLON", "GIBSON", "THADDEUS", "ZAIRE", "COLEMAN", "RODERICK",
    "JABARI", "ZACKERY", "AGUSTIN", "ALFRED", "ARLO", "BRAYLIN",
    "LEIGHTON", "TURNER", "ARIAN", "CLINTON", "LEGEND", "MILLER",
    "QUINTEN", "MUSTAFA", "JAKOBE", "LATHAN", "OTTO", "BLAISE",
    "VIHAAN", "ENOCH", "ROSS", "BRICE", "HOUSTON", "REY",
    "BENTON", "BODHI", "GRAYSEN", "JOHANN", "REUBEN", "CREW",
    "DARRYL", "DONTE", "FLYNN", "JAYCOB", "JEAN", "MAXTON",
    "ANDERS", "HUGH", "IGNACIO", "RALPH", "TRYSTAN", "DEVAN",
    "FRANCO", "MARIANO", "TYREE", "BRIDGER", "HOWARD", "JAYDAN",
    "BRECKEN", "JOZIAH", "VALENTIN", "BRODERICK", "MAXX", "ELIAN",
    "ELISEO", "HAIDEN", "TYRESE", "ZEKE", "KEON", "MAKSIM",
    "COEN", "CRISTIANO", "HENDRIX", "DAMARI", "PRINCETON", "DAVON",
    "DEON", "KAEL", "DIMITRI", "JARON", "JAYDIN", "KYAN",
    "CORBAN", "KINGSLEY", "MAJOR", "PIERRE", "YEHUDA", "CAYSON",
    "DANGELO", "JERAMIAH", "KAMREN", "KOHEN", "CAMILO", "CORTEZ",
    "KEYON", "MALAKI", "ETHEN", "SOPHIA", "ISABELLA", "EMMA",
    "OLIVIA", "AVA", "EMILY", "ABIGAIL", "MADISON", "MIA",
    "CHLOE", "ELIZABETH", "ELLA", "ADDISON", "NATALIE", "LILY",
    "GRACE", "SAMANTHA", "AVERY", "SOFIA", "AUBREY", "BROOKLYN",
    "LILLIAN", "VICTORIA", "EVELYN", "HANNAH", "ALEXIS", "CHARLOTTE",
    "ZOEY", "LEAH", "AMELIA", "ZOE", "HAILEY", "LAYLA",
    "GABRIELLA", "NEVAEH", "KAYLEE", "ALYSSA", "ANNA", "SARAH",
    "ALLISON", "SAVANNAH", "ASHLEY", "AUDREY", "TAYLOR", "BRIANNA",
    "AALIYAH", "RILEY", "CAMILA", "KHLOE", "CLAIRE", "SOPHIE",
    "ARIANNA", "PEYTON", "HARPER", "ALEXA", "MAKAYLA", "JULIA",
    "KYLIE", "KAYLA", "BELLA", "KATHERINE", "LAUREN", "GIANNA",
    "MAYA", "SYDNEY", "SERENITY", "KIMBERLY", "MACKENZIE", "AUTUMN",
    "JOCELYN", "FAITH", "LUCY", "STELLA", "JASMINE", "MORGAN",
    "ALEXANDRA", "TRINITY", "MOLLY", "MADELYN", "SCARLETT", "ANDREA",
    "GENESIS", "EVA", "ARIANA", "MADELINE", "BROOKE", "CAROLINE",
    "BAILEY", "MELANIE", "KENNEDY", "DESTINY", "MARIA", "NAOMI",
    "LONDON", "PAYTON", "LYDIA", "ELLIE", "MARIAH", "AUBREE",
    "KAITLYN", "VIOLET", "RYLEE", "LILLY", "ANGELINA", "KATELYN",
    "MYA", "PAIGE", "NATALIA", "RUBY", "PIPER", "ANNABELLE",
    "MARY", "JADE", "ISABELLE", "LILIANA", "NICOLE", "RACHEL",
    "VANESSA", "GABRIELLE", "JESSICA", "JORDYN", "REAGAN", "KENDALL",
    "SADIE", "VALERIA", "BRIELLE", "LYLA", "ISABEL", "BROOKLYNN",
    "REESE", "SARA", "ADRIANA", "ALIYAH", "JENNIFER", "MCKENZIE",
    "GRACIE", "NORA", "KYLEE", "MAKENZIE", "IZABELLA", "LAILA",
    "ALICE", "AMY", "MICHELLE", "SKYLAR", "STEPHANIE", "JULIANA",
    "REBECCA", "JAYLA", "ELEANOR", "CLARA", "GISELLE", "VALENTINA",
    "VIVIAN", "ALAINA", "ELIANA", "ARIA", "VALERIE", "HALEY",
    "ELENA", "CATHERINE", "ELISE", "LILA", "MEGAN", "GABRIELA",
    "DAISY", "JADA", "DANIELA", "PENELOPE", "JENNA", "ASHLYN",
    "DELILAH", "SUMMER", "MILA", "KATE", "KEIRA", "ADRIANNA",
    "HADLEY", "JULIANNA", "MACI", "EDEN", "JOSEPHINE", "AURORA",
    "MELISSA", "HAYDEN", "ALANA", "MARGARET", "QUINN", "ANGELA",
    "BRYNN", "ALIVIA", "KATIE", "RYLEIGH", "KINLEY", "PAISLEY",
    "JORDAN", "ANIYAH", "ALLIE", "MIRANDA", "JACQUELINE", "MELODY",
    "WILLOW", "DIANA", "CORA", "ALEXANDRIA", "MIKAYLA", "DANIELLE",
    "LONDYN", "ADDYSON", "AMAYA", "HAZEL", "CALLIE", "TEAGAN",
    "ADALYN", "XIMENA", "ANGEL", "KINSLEY", "SHELBY", "MAKENNA",
    "ARIEL", "JILLIAN", "CHELSEA", "ALAYNA", "HARMONY", "SIENNA",
    "AMANDA", "PRESLEY", "MAGGIE", "TESSA", "LEILA", "HOPE",
    "GENEVIEVE", "ERIN", "BRIANA", "DELANEY", "ESTHER", "KATHRYN",
    "ANA", "MCKENNA", "CAMILLE", "CECILIA", "LUCIA", "LOLA",
    "LEILANI", "LESLIE", "ASHLYNN", "KAYLEIGH", "ALONDRA", "ALISON",
    "HAYLEE", "CARLY", "JULIET", "LEXI", "KELSEY", "ELIZA",
    "JOSIE", "MARISSA", "MARLEY", "ALICIA", "AMBER", "SABRINA",
    "KAYDENCE", "NORAH", "ALLYSON", "ALINA", "IVY", "FIONA",
    "ISLA", "NADIA", "KYLEIGH", "CHRISTINA", "EMERY", "LAURA",
    "CHEYENNE", "ALEXIA", "EMERSON", "SIERRA", "LUNA", "CADENCE",
    "DANIELLA", "FATIMA", "BIANCA", "CASSIDY", "VERONICA", "KYLA",
    "EVANGELINE", "KAREN", "ADELINE", "JAZMINE", "MALLORY", "ROSE",
    "JAYDEN", "KENDRA", "CAMRYN", "MACY", "ABBY", "DAKOTA",
    "MARIANA", "GIA", "ADELYN", "MADILYN", "JAZMIN", "IRIS",
    "NINA", "GEORGIA", "LILAH", "BREANNA", "KENZIE", "JAYDA",
    "PHOEBE", "LILLIANA", "KAMRYN", "ATHENA", "MALIA", "NYLA",
    "MILEY", "HEAVEN", "AUDRINA", "MADELEINE", "KIARA", "SELENA",
    "MADDISON", "GIULIANA", "EMILIA", "LYRIC", "JOANNA", "ADALYNN",
    "ANNABELLA", "FERNANDA", "AUBRIE", "HEIDI", "ESMERALDA", "KIRA",
    "ELLIANA", "ARABELLA", "KELLY", "KARINA", "PARIS", "CAITLYN",
    "KARA", "RAEGAN", "MIRIAM", "CRYSTAL", "ALEJANDRA", "TATUM",
    "SAVANNA", "TIFFANY", "AYLA", "CARMEN", "MALIYAH", "KARLA",
    "BETHANY", "GUADALUPE", "KAILEY", "MACIE", "GEMMA", "NOELLE",
    "RYLIE", "ELAINA", "LENA", "AMIYAH", "RUTH", "AINSLEY",
    "FINLEY", "DANNA", "PARKER", "EMELY", "JANE", "JOSELYN",
    "SCARLET", "ANASTASIA", "JOURNEY", "ANGELICA", "SASHA", "YARETZI",
    "CHARLIE", "JULIETTE", "LIA", "BRYNLEE", "ANGELIQUE", "KATELYNN",
    "NAYELI", "VIVIENNE", "ADDISYN", "KAELYN", "ANNIE", "TIANA",
    "KYRA", "JANELLE", "CALI", "ALEAH", "CAITLIN", "IMANI",
    "JAYLEEN", "APRIL", "JULIE", "ALESSANDRA", "JULISSA", "KAILYN",
    "JAZLYN", "JANIYAH", "KAYLIE", "MADELYNN", "BAYLEE", "ITZEL",
    "MONICA", "ADELAIDE", "BRYLEE", "MICHAELA", "MADISYN", "CASSANDRA",
    "ELLE", "KAYLIN", "ANIYA", "DULCE", "OLIVE", "JAELYN",
    "COURTNEY", "BRITTANY", "MADALYN", "JASMIN", "KAMILA", "KILEY",
    "TENLEY", "BRAELYN", "HOLLY", "HELEN", "HAYLEY", "CAROLINA",
    "CYNTHIA", "TALIA", "ANYA", "ESTRELLA", "BRISTOL", "JIMENA",
    "HARLEY", "JAMIE", "REBEKAH", "CHARLEE", "LACEY", "JALIYAH",
    "CAMERON", "SARAI", "CAYLEE", "KENNEDI", "DAYANA", "TATIANA",
    "SERENA", "ELOISE", "DAPHNE", "MCKINLEY", "MIKAELA", "CELESTE",
    "HANNA", "LUCILLE", "SKYLER", "NYLAH", "CAMILLA", "LILIAN",
    "LINDSEY", "SAGE", "VIVIANA", "DANICA", "LIANA", "MELANY",
    "AILEEN", "LILLIE", "KADENCE", "ZARIAH", "JUNE", "LILYANA",
    "BRIDGET", "ANABELLE", "LEXIE", "ANAYA", "SKYE", "ALYSON",
    "ANGIE", "PAOLA", "ELSIE", "ERICA", "GRACELYN", "KIERA",
    "MYLA", "AYLIN", "LANA", "PRISCILLA", "KASSIDY", "NATASHA",
    "NIA", "KENLEY", "DYLAN", "KALI", "ADA", "MIRACLE",
    "RAELYNN", "BRIELLA", "EMILEE", "LORELEI", "FRANCESCA", "ARIELLE",
    "MADYSON", "AMIRA", "JAELYNN", "NATALY", "ANNIKA", "JOY",
    "ALANNA", "SHAYLA", "BRENNA", "SLOANE", "VERA", "ABBIGAIL",
    "AMARI", "JAYCEE", "LAURYN", "SKYLA", "WHITNEY", "ASPEN",
    "JOHANNA", "JAYLAH", "NATHALIE", "LANEY", "LOGAN", "BRINLEY",
    "LEIGHTON", "MARLEE", "CIARA", "JUSTICE", "BRENDA", "KAYDEN",
    "ERIKA", "ELISA", "LAINEY", "ROWAN", "ANNABEL", "TERESA",
    "DAHLIA", "JANIYA", "LIZBETH", "NANCY", "ALEENA", "KALIYAH",
    "FARRAH", "MARILYN", "EVE", "ANAHI", "ROSALIE", "JAYLYNN",
    "BAILEE", "EMMALYN", "MADILYNN", "LEA", "SYLVIA", "ANNALISE",
    "AVERIE", "YARELI", "ZOIE", "SAMARA", "AMANI", "REGINA",
    "HAILEE", "ARELY", "EVELYNN", "LUCIANA", "NATALEE", "ANIKA",
    "LIBERTY", "GIANA", "HAVEN", "GLORIA", "GWENDOLYN", "JAZLYNN",
    "MARISOL", "RYAN", "VIRGINIA", "MYAH", "ELSA", "SELAH",
    "MELINA", "ARYANNA", "ADELYNN", "RAELYN", "MIAH", "SARIAH",
    "KAYLYNN", "AMARA", "HELENA", "JAYLEE", "MAEVE", "RAVEN",
    "LINDA", "ANNE", "DESIREE", "MADALYNN", "MEREDITH", "CLARISSA",
    "ELYSE", "MARIE", "ALISSA", "ANABELLA", "HALLIE", "DENISE",
    "ELISABETH", "KAIA", "DANIKA", "KIMORA", "MILAN", "CLAUDIA",
    "DANA", "SIENA", "ZION", "ANSLEY", "SANDRA", "CARA",
    "HALLE", "MALEAH", "MARINA", "SANIYAH", "CASEY", "HARLOW",
    "KASSANDRA", "CHARLEY", "ROSA", "SHILOH", "TORI", "ADELE",
    "KIANA", "ARIELLA", "JAYLENE", "JOSLYN", "KATHLEEN", "AISHA",
    "AMYA", "AYANNA", "ISIS", "KARLEE", "CINDY", "PERLA",
    "JANESSA", "LYLAH", "RAQUEL", "ZARA", "EVIE", "PHOENIX",
    "CATALINA", "LILIANNA", "MOLLIE", "SIMONE", "BRILEY", "BRIA",
    "KRISTINA", "LINDSAY", "ROSEMARY", "CECELIA", "KOURTNEY", "ALIYA",
    "ASIA", "ELIN", "ISABELA", "KRISTEN", "YASMIN", "ALANI",
    "AIYANA", "AMIYA", "FELICITY", "PATRICIA", "KAILEE", "ADRIENNE",
    "ALIANA", "EMBER", "MARIYAH", "MARIAM", "ALLY", "BRYANNA",
    "TABITHA", "WENDY", "SIDNEY", "CLARE", "AIMEE", "LAYLAH",
    "MAIA", "KARSYN", "GRETA", "NOEMI", "JAYDE", "KALLIE",
    "LEANNA", "IRENE", "JESSIE", "PAITYN", "KALEIGH", "LESLY",
    "GRACELYNN", "AMELIE", "ILIANA", "ELAINE", "LILLIANNA", "ELLEN",
    "TARYN", "LAILAH", "RYLAN", "LISA", "EMERSYN", "BRAELYNN",
    "SHANNON", "BEATRICE", "HEATHER", "JAYLIN", "TALIYAH", "ARYA",
    "EMILIE", "ALI", "JANAE", "CHAYA", "CHERISH", "JAIDA",
    "JOURNEE", "SAWYER", "DESTINEE", "EMMALEE", "IVANNA", "CHARLI",
    "JOCELYNN", "KAYA", "ELIANNA", "ARMANI", "KAITLYNN", "RIHANNA",
    "REYNA", "CHRISTINE", "ALIA", "LEYLA", "MCKAYLA", "CELIA",
    "RAINA", "ALAYAH", "MACEY", "MEGHAN", "ZANIYAH", "CAROLYN",
    "KYNLEE", "CARLEE", "ALENA", "BRYN", "JOLIE", "CARLA",
    "EILEEN", "KEYLA", "SANIYA", "LIVIA", "AMINA", "ANGELINE",
    "KRYSTAL", "ZARIA", "EMELIA", "RENATA", "MERCEDES", "PAULINA",
    "DIAMOND", "JENNY", "AVIANA", "AYLEEN", "BARBARA", "ALISHA",
    "JAQUELINE", "MARYAM", "JULIANNE", "MATILDA", "SONIA", "EDITH",
    "MARTHA", "AUDRIANA", "KAYLYN", "EMMY", "GIADA", "TEGAN",
    "CHARLEIGH", "HALEIGH", "NATHALY", "SUSAN", "KENDAL", "LEIA",
    "JORDYNN", "AMIRAH", "GIOVANNA", "MIRA", "ADDILYN", "FRANCES",
    "KAITLIN", "KYNDALL", "MYRA", "ABBIE", "SAMIYAH", "TARAJI",
    "BRAYLEE", "CORINNE", "JAZMYN", "KAIYA", "LORELAI", "ABRIL",
    "KENYA", "MAE", "HADASSAH", "ALISSON", "HAYLIE", "BRISA",
    "DEBORAH", "MINA", "RAYNE", "AMERICA", "RYANN", "MILANIA",
    "PEARL", "BLAKE", "MILLIE", "DEANNA", "ARACELI", "DEMI",
    "GISSELLE", "PAULA", "KARISSA", "SHARON", "KENSLEY", "RACHAEL",
    "ARYANA", "CHANEL", "NATALYA", "HAYLEIGH", "PALOMA", "AVIANNA",
    "JEMMA", "MORIAH", "RENEE", "ALYVIA", "ZARIYAH", "HANA",
    "JUDITH", "KINSEY", "SALMA", "KENNA", "MARA", "PATIENCE",
    "SAANVI", "CRISTINA", "DIXIE", "KAYLEN", "AVERI", "CARLIE",
    "KIRSTEN", "LILYANNA", "CHARITY", "LARISSA", "ZURI", "CHANA",
    "INGRID", "LINA", "TIANNA", "LILIA", "MARISA", "NAHLA",
    "SHERLYN", "ADYSON", "CAILYN", "PRINCESS", "YOSELIN", "AUBRIANNA",
    "MARITZA", "RAYNA", "LUZ", "CHEYANNE", "AZARIA", "JACEY",
    "ROSELYN", "ELLIOT", "JAIDEN", "TARA", "ALMA", "ESPERANZA",
    "JAKAYLA", "YESENIA", "KIERSTEN", "MARLENE", "NOVA", "ADELINA",
    "AYANA", "KAI", "NOLA", "SLOAN", "AVAH", "CARLEY",
    "MEADOW", "NEVEAH", "TAMIA", "ALAYA", "JADYN", "SANAA",
    "KAILYNN", "DIYA", "RORY", "ABBEY", "KARIS", "MALIAH",
    "BELEN", "BENTLEY", "JAIDYN", "SHANIA", "BRITNEY", "YAZMIN",
    "AUBRI", "MALAYA", "MICAH", "RIVER", "ALANNAH", "JOLENE",
    "SHANIYA", "TIA", "YAMILET", "BRYLEIGH", "CARISSA", "KARLIE",
    "LIBBY", "LILITH", "LARA", "TESS", "ALIZA", "LAUREL",
    "KAELYNN", "LEONA", "REGAN", "YARITZA", "KASEY", "MATTIE",
    "AUDRIANNA", "BLAKELY", "CAMPBELL", "DOROTHY", "JULIETA", "KYLAH",
    "KYNDAL", "TEMPERANCE", "TINLEY", "AKIRA", "SAIGE", "ASHTYN",
    "JEWEL", "KELSIE", "MIYA", "CAMBRIA", "ANALIA", "JANET",
    "KAIRI", "ALEIGHA", "BREE", "DALIA", "LIV", "SARAHI",
    "YAMILETH", "CARLEIGH", "GERALDINE", "IZABELLE", "RIYA", "SAMIYA",
    "ABRIELLE", "ANNABELL", "LEIGHA", "PAMELA", "CAYDENCE", "JOYCE",
    "JUNIPER", "MALAYSIA", "ISABELL", "BLAIR", "JAYLYN", "MARIANNA",
    "RIVKA", "ALIANNA", "GWYNETH", "KENDYL", "SKY", "ESME",
    "JADEN", "SARIYAH", "STACY", "KIMBER", "KAMILLE", "MILAGROS",
    "KARLY", "KARMA", "THALIA", "WILLA", "AMALIA", "HATTIE",
    "PAYTEN", "ANABEL", "ANN", "GALILEA", "MILANA", "YULIANA",
    "DAMARIS"]

surnames = [
    "SMITH", "JOHNSON", "WILLIAMS", "JONES", "BROWN", "DAVIS", "MILLER",
    "WILSON", "MOORE", "TAYLOR", "ANDERSON", "THOMAS", "JACKSON", "WHITE",
    "HARRIS", "MARTIN", "THOMPSON", "GARCIA", "MARTINEZ", "ROBINSON", "CLARK",
    "RODRIGUEZ", "LEWIS", "LEE", "WALKER", "HALL", "ALLEN", "YOUNG", "GRIFFIN",
    "HERNANDEZ", "KING", "WRIGHT", "LOPEZ", "HILL", "SCOTT", "GREEN",
    "ADAMS", "BAKER", "GONZALEZ", "NELSON", "CARTER", "MITCHELL", "PEREZ",
    "ROBERTS", "TURNER", "PHILLIPS", "CAMPBELL", "PARKER", "EVANS", "EDWARDS",
    "COLLINS", "STEWART", "SANCHEZ", "MORRIS", "ROGERS", "REED", "COOK",
    "MORGAN", "BELL", "MURPHY", "BAILEY", "RIVERA", "COOPER", "RICHARDSON",
    "COX", "HOWARD", "WARD", "TORRES", "PETERSON", "GRAY", "RAMIREZ",
    "JAMES", "WATSON", "BROOKS", "KELLY", "SANDERS", "PRICE", "BENNETT",
    "WOOD", "BARNES", "ROSS", "HENDERSON", "COLEMAN", "JENKINS", "PERRY",
    "POWELL", "LONG", "PATTERSON", "HUGHES", "FLORES", "WASHINGTON", "BUTLER",
    "SIMMONS", "FOSTER", "GONZALES", "BRYANT", "ALEXANDER", "RUSSELL",
    "DIAZ", "HAYES", "MYERS", "FORD", "HAMILTON", "GRAHAM", "SULLIVAN",
    "WALLACE", "WOODS", "COLE", "WEST", "JORDAN", "OWENS", "REYNOLDS",
    "FISHER", "ELLIS", "HARRISON", "GIBSON", "MCDONALD", "CRUZ", "MARSHALL",
    "ORTIZ", "GOMEZ", "MURRAY", "FREEMAN", "WELLS", "WEBB", "SIMPSON",
    "STEVENS", "TUCKER", "PORTER", "HUNTER", "HICKS", "CRAWFORD", "HENRY",
    "BOYD", "MASON", "MORALES", "KENNEDY", "WARREN", "DIXON", "RAMOS",
    "REYES", "BURNS", "GORDON", "SHAW", "HOLMES", "RICE", "ROBERTSON",
    "HUNT", "BLACK", "DANIELS", "PALMER", "MILLS", "NICHOLS", "GRANT",
    "KNIGHT", "FERGUSON", "ROSE", "STONE", "HAWKINS", "DUNN", "PERKINS",
    "HUDSON", "SPENCER", "GARDNER", "STEPHENS", "PAYNE", "PIERCE", "BERRY",
    "MATTHEWS", "ARNOLD", "WAGNER", "WILLIS", "RAY", "WATKINS", "OLSON",
    "CARROLL", "DUNCAN", "SNYDER", "HART", "CUNNINGHAM", "BRADLEY", "LANE",
    "ANDREWS", "RUIZ", "HARPER", "FOX", "RILEY", "ARMSTRONG", "CARPENTER",
    "WEAVER", "GREENE", "LAWRENCE", "ELLIOTT", "CHAVEZ", "SIMS", "AUSTIN",
    "PETERS", "KELLEY", "FRANKLIN", "LAWSON", "FIELDS", "GUTIERREZ", "RYAN",
    "SCHMIDT", "CARR", "VASQUEZ", "CASTILLO", "WHEELER", "CHAPMAN", "OLIVER",
    "MONTGOMERY", "RICHARDS", "WILLIAMSON", "JOHNSTON", "BANKS", "MEYER",
    "MCCOY", "HOWELL", "ALVAREZ", "MORRISON", "HANSEN", "FERNANDEZ", "GARZA",
    "HARVEY", "LITTLE", "BURTON", "STANLEY", "NGUYEN", "GEORGE", "JACOBS",
    "REID", "KIM", "FULLER", "LYNCH", "DEAN", "GILBERT", "GARRETT", "BISHOP",
    "ROMERO", "WELCH", "LARSON", "FRAZIER", "BURKE", "HANSON", "DAY",
    "MENDOZA", "MORENO", "BOWMAN", "MEDINA", "FOWLER", "BREWER", "HOFFMAN",
    "CARLSON", "SILVA", "PEARSON", "HOLLAND", "DOUGLAS", "FLEMING", "JENSEN",
    "VARGAS", "BYRD", "DAVIDSON", "HOPKINS", "MAY", "TERRY", "HERRERA",
    "WADE", "SOTO", "WALTERS", "CURTIS", "NEAL", "CALDWELL", "LOWE",
    "JENNINGS", "BARNETT", "GRAVES", "JIMENEZ", "HORTON", "SHELTON", "BARRETT",
    "OBRIEN", "CASTRO", "SUTTON", "GREGORY", "MCKINNEY", "LUCAS", "MILES",
    "CRAIG", "RODRIQUEZ", "CHAMBERS", "HOLT", "LAMBERT", "FLETCHER", "WATTS",
    "BATES", "HALE", "RHODES", "PENA", "BECK", "NEWMAN", "HAYNES",
    "MCDANIEL", "MENDEZ", "BUSH", "VAUGHN", "PARKS", "DAWSON", "SANTIAGO",
    "NORRIS", "HARDY", "LOVE", "STEELE", "CURRY", "POWERS", "SCHULTZ",
    "BARKER", "GUZMAN", "PAGE", "MUNOZ", "BALL", "KELLER", "CHANDLER",
    "WEBER", "LEONARD", "WALSH", "LYONS", "RAMSEY", "WOLFE", "SCHNEIDER",
    "MULLINS", "BENSON", "SHARP", "BOWEN", "DANIEL", "BARBER", "CUMMINGS",
    "HINES", "BALDWIN", "GRIFFITH", "VALDEZ", "HUBBARD", "SALAZAR", "REEVES",
    "WARNER", "STEVENSON", "BURGESS", "SANTOS", "TATE", "CROSS", "GARNER",
    "MANN", "MACK", "MOSS", "THORNTON", "DENNIS", "MCGEE", "FARMER",
    "DELGADO", "AGUILAR", "VEGA", "GLOVER", "MANNING", "COHEN", "HARMON",
    "RODGERS", "ROBBINS", "NEWTON", "TODD", "BLAIR", "HIGGINS", "INGRAM",
    "REESE", "CANNON", "STRICKLAND", "TOWNSEND", "POTTER", "GOODWIN", "WALTON",
    "ROWE", "HAMPTON", "ORTEGA", "PATTON", "SWANSON", "JOSEPH", "FRANCIS",
    "GOODMAN", "MALDONADO", "YATES", "BECKER", "ERICKSON", "HODGES", "RIOS",
    "CONNER", "ADKINS", "WEBSTER", "NORMAN", "MALONE", "HAMMOND", "FLOWERS",
    "COBB", "MOODY", "QUINN", "BLAKE", "MAXWELL", "POPE", "FLOYD", "SANDOVAL",
    "OSBORNE", "PAUL", "MCCARTHY", "GUERRERO", "LINDSEY", "ESTRADA",
    "GIBBS", "TYLER", "GROSS", "FITZGERALD", "STOKES", "DOYLE", "SHERMAN",
    "SAUNDERS", "WISE", "COLON", "GILL", "ALVARADO", "GREER", "PADILLA",
    "SIMON", "WATERS", "NUNEZ", "BALLARD", "SCHWARTZ", "MCBRIDE", "HOUSTON",
    "CHRISTENSEN", "KLEIN", "PRATT", "BRIGGS", "PARSONS", "MCLAUGHLIN",
    "FRENCH", "BUCHANAN", "MORAN", "COPELAND", "ROY", "PITTMAN", "BRADY",
    "MCCORMICK", "HOLLOWAY", "BROCK", "POOLE", "FRANK", "LOGAN", "OWEN",
    "BASS", "MARSH", "DRAKE", "WONG", "JEFFERSON", "PARK", "MORTON",
    "ABBOTT", "SPARKS", "PATRICK", "NORTON", "HUFF", "CLAYTON", "MASSEY",
    "LLOYD", "FIGUEROA", "CARSON", "BOWERS", "ROBERSON", "BARTON", "TRAN",
    "LAMB", "HARRINGTON", "CASEY", "BOONE", "CORTEZ", "CLARKE", "MATHIS",
    "SINGLETON", "WILKINS", "CAIN", "BRYAN", "UNDERWOOD", "HOGAN", "MCKENZIE",
    "COLLIER", "LUNA", "PHELPS", "MCGUIRE", "ALLISON", "BRIDGES", "WILKERSON",
    "NASH", "SUMMERS", "ATKINS", "WILCOX", "PITTS", "CONLEY", "MARQUEZ",
    "BURNETT", "RICHARD", "COCHRAN", "CHASE", "DAVENPORT", "HOOD", "GATES",
    "CLAY", "AYALA", "SAWYER", "ROMAN", "VAZQUEZ", "DICKERSON", "HODGE",
    "ACOSTA", "FLYNN", "ESPINOZA", "NICHOLSON", "MONROE", "WOLF", "MORROW",
    "KIRK", "RANDALL", "ANTHONY", "WHITAKER", "OCONNOR", "SKINNER", "WARE",
    "MOLINA", "KIRBY", "HUFFMAN", "BRADFORD", "CHARLES", "GILMORE",
    "ONEAL", "BRUCE", "LANG", "COMBS", "KRAMER", "HEATH", "HANCOCK",
    "GALLAGHER", "GAINES", "SHAFFER", "SHORT", "WIGGINS", "MATHEWS", "MCCLAIN",
    "FISCHER", "WALL", "SMALL", "MELTON", "HENSLEY", "BOND", "DYER",
    "CAMERON", "GRIMES", "CONTRERAS", "CHRISTIAN", "WYATT", "BAXTER", "SNOW",
    "MOSLEY", "SHEPHERD", "LARSEN", "HOOVER", "BEASLEY", "GLENN", "PETERSEN",
    "WHITEHEAD", "MEYERS", "KEITH", "GARRISON", "VINCENT", "SHIELDS", "HORN",
    "SAVAGE", "OLSEN", "SCHROEDER", "HARTMAN", "WOODARD", "MUELLER", "KEMP",
    "DELEON", "BOOTH", "PATEL", "CALHOUN", "WILEY", "EATON", "CLINE",
    "NAVARRO", "HARRELL", "LESTER", "HUMPHREY", "PARRISH", "DURAN",
    "HUTCHINSON", "ZIMMERMAN", "DOMINGUEZ", "MCINTOSH", "RAYMOND",
    "HESS", "DORSEY", "BULLOCK", "ROBLES", "BEARD", "DALTON", "AVILA",
    "VANCE", "RICH", "BLACKWELL", "YORK", "JOHNS", "BLANKENSHIP", "TREVINO",
    "SALINAS", "CAMPOS", "PRUITT", "MOSES", "CALLAHAN", "GOLDEN", "MONTOYA",
    "HARDIN", "GUERRA", "MCDOWELL", "CAREY", "STAFFORD", "GALLEGOS", "HENSON",
    "WILKINSON", "BOOKER", "MERRITT", "MIRANDA", "ATKINSON", "ORR", "DECKER",
    "HOBBS", "PRESTON", "TANNER", "KNOX", "PACHECO", "STEPHENSON", "GLASS",
    "ROJAS", "SERRANO", "MARKS", "HICKMAN", "ENGLISH", "SWEENEY", "STRONG",
    "PRINCE", "MCCLURE", "CONWAY", "WALTER", "ROTH", "MAYNARD", "FARRELL",
    "LOWERY", "HURST", "NIXON", "WEISS", "TRUJILLO", "ELLISON", "SLOAN",
    "JUAREZ", "WINTERS", "MCLEAN", "RANDOLPH", "LEON", "BOYER", "VILLARREAL",
    "MCCALL", "GENTRY", "CARRILLO", "KENT", "AYERS", "LARA", "SHANNON",
    "SEXTON", "PACE", "HULL", "LEBLANC", "BROWNING", "VELASQUEZ", "LEACH",
    "CHANG", "HOUSE", "SELLERS", "HERRING", "NOBLE", "FOLEY", "BARTLETT",
    "MERCADO", "LANDRY", "DURHAM", "WALLS", "BARR", "MCKEE", "BAUER",
    "RIVERS", "EVERETT", "BRADSHAW", "PUGH", "VELEZ", "RUSH", "ESTES",
    "DODSON", "MORSE", "SHEPPARD", "WEEKS", "CAMACHO", "BEAN", "BARRON",
    "LIVINGSTON", "MIDDLETON", "SPEARS", "BRANCH", "BLEVINS", "CHEN", "KERR",
    "MCCONNELL", "HATFIELD", "HARDING", "ASHLEY", "SOLIS", "HERMAN", "FROST",
    "GILES", "BLACKBURN", "WILLIAM", "PENNINGTON", "WOODWARD", "FINLEY",
    "KOCH", "BEST", "SOLOMON", "MCCULLOUGH", "DUDLEY", "NOLAN", "BLANCHARD",
    "RIVAS", "BRENNAN", "MEJIA", "KANE", "BENTON", "JOYCE", "BUCKLEY",
    "HALEY", "VALENTINE", "MADDOX", "RUSSO", "MCKNIGHT", "BUCK", "MOON",
    "MCMILLAN", "CROSBY", "BERG", "DOTSON", "MAYS", "ROACH", "CHURCH",
    "CHAN", "RICHMOND", "MEADOWS", "FAULKNER", "ONEILL", "KNAPP", "KLINE",
    "BARRY", "OCHOA", "JACOBSON", "GAY", "AVERY", "HENDRICKS", "HORNE",
    "SHEPARD", "HEBERT", "CHERRY", "CARDENAS", "MCINTYRE", "WHITNEY", "WALLER",
    "HOLMAN", "DONALDSON", "CANTU", "TERRELL", "MORIN", "GILLESPIE", "FUENTES",
    "TILLMAN", "SANFORD", "BENTLEY", "PECK", "KEY", "SALAS", "ROLLINS",
    "GAMBLE", "DICKSON", "BATTLE", "SANTANA", "CABRERA", "CERVANTES", "HOWE",
    "HINTON", "HURLEY", "SPENCE", "ZAMORA", "YANG", "MCNEIL", "SUAREZ",
    "CASE", "PETTY", "GOULD", "MCFARLAND", "SAMPSON", "CARVER", "BRAY",
    "ROSARIO", "MACDONALD", "STOUT", "HESTER", "MELENDEZ", "DILLON", "FARLEY",
    "HOPPER", "GALLOWAY", "POTTS", "BERNARD", "JOYNER", "STEIN", "AGUIRRE",
    "OSBORN", "MERCER", "BENDER", "FRANCO", "ROWLAND", "SYKES", "BENJAMIN",
    "TRAVIS", "PICKETT", "CRANE", "SEARS", "MAYO", "DUNLAP", "HAYDEN",
    "WILDER", "MCKAY", "COFFEY", "MCCARTY", "EWING", "COOLEY", "VAUGHAN",
    "BONNER", "COTTON", "HOLDER", "STARK", "FERRELL", "CANTRELL", "FULTON",
    "LYNN", "LOTT", "CALDERON", "ROSA", "POLLARD", "HOOPER", "BURCH",
    "MULLEN", "FRY", "RIDDLE", "LEVY", "DAVID", "DUKE", "ODONNELL",
    "GUY", "MICHAEL", "BRITT", "FREDERICK", "DAUGHERTY", "BERGER", "DILLARD",
    "ALSTON", "JARVIS", "FRYE", "RIGGS", "CHANEY", "ODOM", "DUFFY",
    "FITZPATRICK", "VALENZUELA", "MERRILL", "MAYER", "ALFORD", "MCPHERSON",
    "ACEVEDO", "DONOVAN", "BARRERA", "ALBERT", "COTE", "REILLY", "COMPTON",
    "MOONEY", "MCGOWAN", "CRAFT", "CLEVELAND", "CLEMONS", "WYNN", "NIELSEN",
    "BAIRD", "STANTON", "SNIDER", "ROSALES", "BRIGHT", "WITT", "STUART",
    "HAYS", "HOLDEN", "RUTLEDGE", "KINNEY", "CLEMENTS", "CASTANEDA", "SLATER",
    "HAHN", "EMERSON", "CONRAD", "BURKS", "DELANEY", "PATE", "LANCASTER",
    "SWEET", "JUSTICE", "TYSON", "SHARPE", "WHITFIELD", "TALLEY", "MACIAS",
    "IRWIN", "BURRIS", "RATLIFF", "MCCRAY", "MADDEN", "KAUFMAN", "BEACH",
    "GOFF", "CASH", "BOLTON", "MCFADDEN", "LEVINE", "GOOD", "BYERS",
    "KIRKLAND", "KIDD", "WORKMAN", "CARNEY", "DALE", "MCLEOD", "HOLCOMB",
    "ENGLAND", "FINCH", "HEAD", "BURT", "HENDRIX", "SOSA", "HANEY",
    "FRANKS", "SARGENT", "NIEVES", "DOWNS", "RASMUSSEN", "BIRD", "HEWITT",
    "LINDSAY", "LE", "FOREMAN", "VALENCIA", "ONEIL", "DELACRUZ", "VINSON",
    "DEJESUS", "HYDE", "FORBES", "GILLIAM", "GUTHRIE", "WOOTEN", "HUBER",
    "BARLOW", "BOYLE", "MCMAHON", "BUCKNER", "ROCHA", "PUCKETT", "LANGLEY",
    "KNOWLES", "COOKE", "VELAZQUEZ", "WHITLEY", "NOEL", "VANG"]


def randomNums(num, count):
    while True:
        nums = []
        for i in range(count - 1):
            nums.append(random.randrange(1, num - 1))
        if sum(nums) < num:
            nums.append(num - sum(nums))
            return nums


def password(ip):
    return md5.md5(ip + "PASSWSLON").hexdigest()

def login(ip):
    return md5.md5(ip + "LOGINSLON").hexdigest()


def read_line_from_socket(s):
    ret = ""
    while True:
        c = s.recv(1)
        ret += c
        if c == "\n":
            break
    return ret


def check(ip):
    text_list = []
    text_list.append("AU %s %s FALSE" % ("AGENT", "SUPERPASS"))
    text_list.append("AU %s %s TRUE" % ("booking", "booking"))
    text_list.append("AU %s %s FALSE" % (login(ip), password(ip)))

    #Add flights
    for i in range(10):
        city_org, city_dst = random.sample(cities, 2)
        airline = random.choice(airlines)
        flight_num = random.randrange(0, 10000)
        date = random.randrange(1353747600, 1354352400, 300)
        date_s = time.strftime("%m%d%y", time.gmtime(date))
        time_s = time.strftime("%H%M", time.gmtime(date))
        c = random.sample(classes, 5)
        nums = randomNums(200, 5)
        rand_nums = [random.randrange(100, 1993) for i in range(5)]
        classes_s1 = ",".join(["%s:%d:%d" % (c[i], nums[i], rand_nums[i]) for i in range(5)])
        text_list.append("AF %s %d %s %s %s %s %s" % (airline, flight_num, city_org, city_dst, date_s, time_s, classes_s1))

    #Add hotels
    for i in range(10):
        chain = random.choice(airlines)
        name = random.choice(names)
        city = random.choice(cities)
        date = random.randrange(1353747600, 1354352400, 300)
        date_s = time.strftime("%m%d%y", time.gmtime(date))
        c = random.sample(classes, 5)
        nums = randomNums(200, 5)
        rand_nums = [random.randrange(100, 1993) for i in range(5)]
        classes_s1 = ",".join(["%s:%d:%d" % (c[i], nums[i], rand_nums[i]) for i in range(5)])
        text_list.append("AH %s %s %s %s %s" % (chain, name, city, date_s, classes_s1))

    text = "".join(text_list)

    cert = load_key("priv.pem")
    data_hash = hashlib.sha1(text).digest()
    sign = cert.sign(data_hash)

    #Send system commands
    s = socket.create_connection((ip, PORT), TIMEOUT)
    s.sendall("BA %d %s\n" % (len(text_list), sign.encode("hex")))
    for line in text_list:
        s.sendall(line + "\n")
    s.close()

    #Test common fucntions
    s = socket.create_connection((ip, PORT), TIMEOUT)

    s.sendall("JI AGENT SUPERPASS\n")
    read_line_from_socket(s)

    s.sendall("A N\n")

    lines = []
    while True:
        line = read_line_from_socket(s).strip()
        if not line:
            break
        lines.append(line)
    lines = lines[1:]
    successC = None
    lineNum = 1
    for line in lines:
        fields = line.split()[4:-3]
        for f in fields:
            c = f[0]
            count = int(f[1:])
            if count != 0:
                successC = c
                break
        if successC is not None:
            break
        lineNum += 1

    s.sendall("SS 1 %s %d\n" % (successC, lineNum))
    read_line_from_socket(s)

    name = random.choice(names)
    surname = random.choice(surnames)

    s.sendall("NM %s %s\n" % (name, surname))
    read_line_from_socket(s)

    s.sendall("ET\n")
    et_line = read_line_from_socket(s).strip().split(" ")[-1]

    s.sendall("RT %s\n" % et_line)
    rt_line = read_line_from_socket(s)

    if rt_line.find(name) == -1 or rt_line.find(surname) == -1:
        sys.stderr.write( rt_line )
        sys.exit( MUMBLE )
    s.close()
    sys.exit(OK)


def put(ip, flag_id, flag):
    #print("put %s %s %s" % (ip, flag_id, flag))

    city = random.choice(cities)

    s = socket.create_connection((ip, PORT), TIMEOUT)
    s.sendall("JI %s %s\n" % (login(ip), password(ip)))
    read_line_from_socket(s)
    s.sendall("HA \n")

    lines = []
    while True:
        line = read_line_from_socket(s).strip()
        if not line:
            break
        lines.append(line)
    lines = lines[1:]

    successC = None
    lineNum = 1
    for line in lines:
        fields = line.split()[4:10]
        for f in fields:
            c = f[0]
            count = int(f[1:])
            if count != 0:
                successC = c
                break
        if successC is not None:
            break
        lineNum += 1

    s.sendall("SH 1 %s %d\n" % (successC, lineNum))
    read_line_from_socket(s)

    name = random.choice(names)
    surname = random.choice(surnames)
    s.sendall("NM %s %s MR %s\n" % (surname, name, flag))

    check_line = read_line_from_socket(s).strip()
    if name not in check_line or surname not in check_line:
        sys.stderr.write(check_line)
        sys.exit(MUMBLE)

    s.sendall("ET\n")

    et_line = read_line_from_socket(s).strip().split(" ")[-1]
    s.close()

    print et_line

    sys.exit(OK)


def get(ip, flag_id, flag):
    #print("get %s %s %s" % (ip, flag_id, flag))

    s = socket.create_connection((ip, PORT), TIMEOUT)

    s.sendall("JI %s %s\n" % (login(ip), password(ip)))
    read_line_from_socket(s)
    s.sendall("RT %s\n" % flag_id)

    line = read_line_from_socket(s).strip()
    s.close()

    if line.find( flag.upper() ) != -1:
        print "OK"
        sys.exit(OK)
    else:
        print "NO FLAG"
        sys.exit(NOFLAG)


### START ###
try:
    mode = sys.argv[1]

    if mode not in ('check', 'put', 'get'):
        sys.exit(INTERNALERROR)

    ret = INTERNALERROR
    if mode == 'check':
        ip = sys.argv[2]
        ret = check(ip)
    elif mode == 'put':
        ip, flag_id, flag = sys.argv[2:5]
        ret = put(ip, flag_id, flag)
    elif mode == 'get':
        ip, flag_id, flag = sys.argv[2:5]
        ret = get(ip, flag_id, flag)
    sys.exit(ret)
except socket.error as E:
    print E
    # if connection reset by peer
    if E.errno == errno.ECONNRESET:
        sys.stderr.write( "connection reset by peer" )
        sys.exit(MUMBLE)
    else:
        sys.exit(NOCONNECT)
except ValueError as E:
    print("WRONG ARGS")
    sys.exit(INTERNALERROR)
except IndexError as E:
    print("WRONG ARGS")
    sys.exit(INTERNALERROR)
except Exception as E:
    sys.stderr.write( str(E) )
    sys.exit(MUMBLE)
