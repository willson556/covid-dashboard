import Application from '@ember/application';
import Resolver from 'ember-resolver';
import loadInitializers from 'ember-load-initializers';
import config from './config/environment';
import 'date-input-polyfill';
import * as Sentry from '@sentry/browser'
import { Ember as EmberIntegration } from '@sentry/integrations';

export default class App extends Application {
    modulePrefix = config.modulePrefix;
    podModulePrefix = config.podModulePrefix;
    Resolver = Resolver;
}

Sentry.init({
    dsn: 'https://16355f27429d467fb4a83f80691737ad@o416772.ingest.sentry.io/5313239',
    integrations: [new EmberIntegration()]
});

loadInitializers(App, config.modulePrefix);