"""Facilitate caching of plot data"""
from dclab.kde import KernelDensityEstimator

from . import util


def get_contour_data(rtdc_ds, xax, yax, xacc, yacc, xscale, yscale,
                     kde_type="histogram", kde_kwargs=None, quantiles=None):
    if kde_kwargs is None:
        kde_kwargs = {}
    rtdc_ds.apply_filter()
    cfg = rtdc_ds.config
    tohash = [
        rtdc_ds.identifier, rtdc_ds.filter.all,
        cfg.get("calculation", ""),
        xax, yax, xacc, yacc, xscale, yscale,
        kde_type, kde_kwargs]
    shash = util.hashobj(tohash)
    if shash in cache_data:
        contours = cache_data[shash]
    else:
        # compute contour plot data
        kde_instance = KernelDensityEstimator(rtdc_ds=rtdc_ds)
        contours = kde_instance.get_contour_lines(
            quantiles=quantiles,
            xax=xax,
            yax=yax,
            xacc=xacc,
            yacc=yacc,
            xscale=xscale,
            yscale=yscale,
            kde_type=kde_type,
            kde_kwargs=kde_kwargs)
        # save in cache
        cache_data[shash] = contours
    return contours


def get_scatter_data(rtdc_ds, downsample, xax, yax, xscale, yscale,
                     kde_type="histogram", kde_kwargs=None):
    if kde_kwargs is None:
        kde_kwargs = {}
    rtdc_ds.apply_filter()
    cfg = rtdc_ds.config
    tohash = [
        rtdc_ds.identifier, rtdc_ds.filter.all, downsample,
        cfg.get("calculation", ""),
        xax, yax, xscale, yscale, kde_type, kde_kwargs]
    shash = util.hashobj(tohash)
    if shash in cache_data:
        x, y, kde, idx = cache_data[shash]
    else:
        # compute scatter plot data
        x, y, idx = rtdc_ds.get_downsampled_scatter(
            xax=xax,
            yax=yax,
            downsample=downsample,
            xscale=xscale,
            yscale=yscale,
            remove_invalid=True,
            ret_mask=True)
        # kde
        kde = rtdc_ds.get_kde_scatter(
            xax=xax,
            yax=yax,
            positions=(x, y),
            kde_type=kde_type,
            kde_kwargs=kde_kwargs,
            xscale=xscale,
            yscale=yscale)
        if kde.size and kde.min() != kde.max():
            kde -= kde.min()
            kde /= kde.max()
        # save in cache
        cache_data[shash] = x, y, kde, idx
    return x, y, kde, idx


cache_data = {}
