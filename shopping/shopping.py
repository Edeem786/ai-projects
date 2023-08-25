import csv
import sys
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    # Administrative(0), Informational(2), ProductRelated(4), Month(10), OperatingSystems(11), 
    # Browser(12), Region(13), TrafficType(14), VisitorType(15), and Weekend(16) should all be of type int
    ints = [0, 2, 4, 11, 12, 13, 14]
    
    # Administrative_Duration(1), Informational_Duration(3), ProductRelated_Duration(5), BounceRates(6), 
    # ExitRates(7), PageValues(8), and SpecialDay(9) should all be of type float.

    floats = [1, 3, 5, 6, 7, 8, 9]

    months = {
        "Jan": 0,
        "Feb": 1,
        "Mar": 2,
        "Apr": 3,
        "May": 4,
        "June": 5,
        "Jul": 6,
        "Aug": 7,
        "Sep": 8,
        "Oct": 9,
        "Nov": 10,
        "Dec": 11
    }

    with open(filename) as f:
        reader = csv.reader(f)
        next(reader) # ignore header
        evidence = []
        labels = []
        for row in reader:
            for column in ints:
                row[column] = int(row[column])

            for column in floats:
                row[column] = float(row[column])

            # Month should be 0 for January, 1 for February, 2 for March, etc. up to 11 for December
            row[10] = months[row[10]]

            # visitor type(15)
            if row[15] == "Returning_Visitor":
                row[15] = 1
            else:
                row[15] = 0
            
            # weekend(16)
            if row[16] == "TRUE":
                row[16] = 1
            else:
                row[16] = 0

            # change labels to integer
            if row[17] == "TRUE":
                row[17] = 1
            else:
                row[17] = 0

            evidence.append(row[:-1])
            labels.append(row[-1])
    
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier()
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positive = 0
    Fpositive = 0
    negative = 0
    Fnegative = 0
    for actual, predicted in zip(labels, predictions):
        if actual == predicted:
            if actual == 1:
                positive += 1
            else:
                negative += 1
        else:
            if actual == 1:
                Fnegative += 1
            else:
                Fpositive += 1
    
    true_pos_rate = positive / (positive + Fnegative)
    true_neg_rate = negative / (negative + Fpositive)
    return (true_pos_rate, true_neg_rate)
    


if __name__ == "__main__":
    main()
