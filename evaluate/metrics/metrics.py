import click
import pandas as pd

from sklearn import metrics

# options


@click.command()
@click.option('--input',
              'input_file',
              required=True,
              type=click.Path(exists=True, readable=True),
              help='Input file with label and predictions')
@click.option('--label-column',
              'label_column',
              required=True,
              type=str,
              help='Column name of the labels')
@click.option('--positive-label',
              'pos_label',
              required=True,
              type=int,
              help='The positive label')
@click.option('--prediction-column',
              'prediction_column',
              required=True,
              type=str,
              help='Column name of the predictions')
@click.option('--output',
              'output_file',
              required=True,
              type=click.Path(writable=True),
              help='Output file with AUCs.')
def cli(input_file, label_column, pos_label, prediction_column, output_file):

    df = pd.read_csv(input_file, delimiter="\t")

    binary_prediction = df[prediction_column].round().astype(int)
    acc = metrics.accuracy_score(df[label_column], binary_prediction, normalize=True)
    acc_bal = metrics.balanced_accuracy_score(df[label_column], binary_prediction)
    f1 = metrics.f1_score(df[label_column], binary_prediction)

    fpr, tpr, thresholds = metrics.roc_curve(df[label_column], df[prediction_column], pos_label=pos_label)
    auroc = metrics.auc(fpr, tpr)

    auprc = metrics.average_precision_score(df[label_column], df[prediction_column], pos_label=pos_label)

    pd.DataFrame(
        data={
            "metric": ["AUROC", "AUPRC", "Accuracy", "Balanced Accuracy", "F1-score"],
            "value": [auroc, auprc, acc, acc_bal, f1]}).to_csv(
        output_file, header=True, index=False, sep="\t", float_format='%.3f'
    )


if __name__ == '__main__':
    cli()
