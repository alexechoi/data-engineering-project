{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "779b9408",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collecting pyarrow\n",
      "  Downloading pyarrow-11.0.0-cp38-cp38-macosx_10_14_x86_64.whl (24.4 MB)\n",
      "\u001b[K     |████████████████████████████████| 24.4 MB 22.1 MB/s eta 0:00:01\n",
      "\u001b[?25hRequirement already satisfied: numpy>=1.16.6 in ./opt/anaconda3/lib/python3.8/site-packages (from pyarrow) (1.20.1)\n",
      "Installing collected packages: pyarrow\n",
      "Successfully installed pyarrow-11.0.0\n",
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    }
   ],
   "source": [
    "pip install pyarrow"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "ef2d3228",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "   cart_id  product_id\n",
      "0        1           1\n",
      "1        1           5\n",
      "2        2           2\n",
      "3        2           2\n",
      "4        2           8\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "# Read parquet file into a pandas DataFrame\n",
    "df = pd.read_parquet('/Users/laratekbas/Desktop/cart_product.parquet')\n",
    "\n",
    "# Print the first 5 rows of the DataFrame\n",
    "print(df.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5c358c8a",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
