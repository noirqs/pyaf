import pyaf.Bench.TS_datasets as tsds
import pyaf.tests.artificial.process_artificial_dataset as art




dataset = tsds.generate_random_TS(N = 32 , FREQ = 'D', seed = 0, trendtype = "constant", cycle_length = 0, transform = "inv", sigma = 0.0, exog_count = 0, ar_order = 12);

art.process_dataset(dataset);