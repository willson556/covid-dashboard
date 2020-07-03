import Model, { attr, hasMany } from '@ember-data/model';

export default class StateModel extends Model {
    @attr name;
    @attr abbrev;
    @attr population;
    @hasMany('county') counties;
}
