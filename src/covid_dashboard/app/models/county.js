import Model, { attr, belongsTo } from '@ember-data/model';

export default class CountyModel extends Model {
    @attr name;
    @attr population;
    @attr disclaimer;
    @belongsTo('state') state;
}