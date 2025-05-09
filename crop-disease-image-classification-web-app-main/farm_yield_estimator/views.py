from django.shortcuts import render
import numpy as np
from scipy import stats
import math

def yield_estimation_view(request):
    context = {}
    
    if request.method == 'POST':
        try:
            N = int(request.POST['tree_count'])
            confidence_level = float(request.POST['confidence_level'])
            margin_of_error = float(request.POST['margin_of_error'])
            estimated_std = float(request.POST['estimated_std'])

            if N <= 0:
                context['error'] = "Number of trees must be positive."
                return render(request, 'farm_estimator/estimate.html', context)

            if N == 1:
                weight = float(request.POST['weight_single_tree'])
                context['single_tree_result'] = weight
                return render(request, 'farm_estimator/estimate.html', context)

            # Sample size calculation
            Z = stats.norm.ppf(1 - (1 - confidence_level)/2)
            n = ((Z**2) * (estimated_std**2)) / (margin_of_error**2)
            n_adjusted = n / (1 + (n/N))
            n_final = min(math.ceil(n_adjusted), N)
            context['required_sample_size'] = n_final

            if 'sample_weights' in request.POST:
                sample_weights_raw = request.POST['sample_weights']
                weights = [float(w.strip()) for w in sample_weights_raw.split(',')][:n_final]
                if len(weights) < n_final:
                    context['error'] = f"Please enter at least {n_final} sample weights."
                    return render(request, 'farm_estimator/estimate.html', context)

                sample_mean = np.mean(weights)
                sample_std = np.std(weights, ddof=1)
                alpha = 1 - confidence_level
                df = len(weights) - 1
                t_value = stats.t.ppf(1 - alpha/2, df)
                fpc = math.sqrt((N - len(weights)) / (N - 1)) if N > 1 else 1
                std_error = (sample_std / math.sqrt(len(weights))) * fpc
                moe = t_value * std_error

                context.update({
                    'sample_mean': sample_mean,
                    'sample_std': sample_std,
                    'moe': moe,
                    'ci_low': sample_mean - moe,
                    'ci_high': sample_mean + moe,
                    'total_estimate': sample_mean * N,
                    'total_ci_low': N * (sample_mean - moe),
                    'total_ci_high': N * (sample_mean + moe),
                })

        except Exception as e:
            context['error'] = str(e)

    return render(request, 'farm_yield_estimator/estimate.html', context)
