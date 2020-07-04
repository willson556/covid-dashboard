import Ember from 'ember';
import Controller from '@ember/controller';
import QueryParams from 'ember-parachute';

export const myQueryParams = new QueryParams({
    'config.states': {
        defaultValue: []
    },
    'config.counties': {
        defaultValue: []
    },
    'config.plots': {
        defaultValue: []
    },
    'config.startDate': {
        defaultValue: "2020-03-01"
    },
    'config.endDate': {
        defaultValue: new Date().toISOString().substring(0,10)
    },
    'config.perCapita': {
        defaultValue: true
    }
});

const { service } = Ember.inject;

export default Controller.extend(myQueryParams.Mixin, {
    config: service()
});
