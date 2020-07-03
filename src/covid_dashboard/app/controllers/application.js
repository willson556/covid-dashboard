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
});

const { service } = Ember.inject;

export default Controller.extend(myQueryParams.Mixin, {
    config: service()
});
