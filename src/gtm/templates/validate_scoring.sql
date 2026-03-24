-- ============================================================
-- Validation query: company_scoring_v4 logistic regression
-- Source: ml.company_scoring_data_v4 (has ALL features incl. event-level)
-- Replicates the sGTM JS model in SQL for comparison.
-- JIRA: DATA-375
-- ============================================================

WITH model AS (
  SELECT
    d.domain,
    d.tld,
    d.net_revenue_first_transport,
    d.distance_first_transport,
    d.transport_type_first_transport,
    d.vehicle_type_first_transport,
    CAST(d.online AS STRING) AS online,
    d.payment_method,
    d.shipper_language,
    d.loading_country_code,
    d.unloading_country_code,
    d.orders_total,
    d.min_3_orders,

    -- ============================================================
    -- z = INTERCEPT
    -- ============================================================
    0.19609285288872272

    -- ============================================================
    -- NUMERIC: net_revenue_first_transport (standardized)
    -- ============================================================
    + 0.00001107061766784912 * (COALESCE(d.net_revenue_first_transport, 366.1414280793821) - 366.1414280793821) / 321.82600082883715

    -- NUMERIC: distance_first_transport (standardized)
    + 0.00006323441850322997 * (COALESCE(d.distance_first_transport, 316.16649780479764) - 316.16649780479764) / 320.1420009659045

    -- ============================================================
    -- NUMERIC: NACE one-hot (standardized)
    -- ============================================================
    + -0.3724418399822121  * (d.a - 0.007880220646178123) / 0.08842512646147806
    + -0.06417412913497608 * (d.b - 0.0020263424518743647) / 0.044971814130477954
    + -0.2632725211672573  * (d.c - 0.2289766970618035) / 0.4201978654581521
    + -0.49517150148598943 * (d.d - 0.006304176516942455) / 0.07915263211543014
    + -0.3233593619270897  * (d.e - 0.010919734323989686) / 0.1039312740431183
    + -0.31192458934273726 * (d.f - 0.08656985252729928) / 0.2812195157802441
    + -0.33773296920594353 * (d.g - 0.11910390633794907) / 0.3239289710434889
    + -0.1137643669608994  * (d.h - 0.03320950129460761) / 0.179193317720695
    + -0.3504966677499206  * (d.i - 0.01531014296971746) / 0.12279022692555953
    + -0.2760497540103016  * (d.j - 0.020038275357424258) / 0.14013905139219598
    + -0.26846351745026564 * (d.k - 0.06022740065293277) / 0.2379210652906047
    + -0.42024230124900225 * (d.l - 0.01114488348530901) / 0.10498531252019136
    + -0.4108003711413672  * (d.m - 0.01564786671169644) / 0.12411585378909575
    + -0.298967049218506   * (d.n - 0.1794438815715416) / 0.38374516636764844
    + -0.23946870367145703 * (d.o - 0.05516154452324664) / 0.22830816112415636
    + -0.44168843033004374 * (d.p - 0.002701789935832494) / 0.051911401755666726
    + -0.31568583174643416 * (d.q - 0.022965214454576104) / 0.1498009999681272
    + -0.32659569463848465 * (d.r - 0.015422717550377125) / 0.1232337898270804
    + -0.39376798196052365 * (d.s - 0.01879995497016775) / 0.13582559959729631
    + -0.34740888783379653 * (d.t - 0.016661037937633627) / 0.12800504802501472
    + -0.4716439511463671  * (d.u - 0.00011257458065968654) / 0.01061011690132048

    -- ============================================================
    -- CATEGORICAL: company profile
    -- ============================================================
    + CASE LOWER(d.no_shipping_required)       WHEN 'false' THEN 0.023170144583303243 WHEN 'true' THEN -0.2100050877451799 WHEN 'unknown' THEN -0.21668976294307804 ELSE 0 END
    + CASE LOWER(d.b2b_business_model)         WHEN 'false' THEN -0.12742904380817627 WHEN 'true' THEN -0.03191401420500469 WHEN 'unknown' THEN -0.09014046223464109 ELSE 0 END
    + CASE LOWER(d.logistics_transportation)   WHEN 'false' THEN -0.09141360555907964 WHEN 'true' THEN 0.15029359800121406 WHEN 'unknown' THEN -0.056748765001659054 ELSE 0 END
    + CASE LOWER(d.min_200_employees)          WHEN 'false' THEN -0.20322449080190091 WHEN 'true' THEN -0.005473507280983768 WHEN 'unknown' THEN 0.01228560443283689 ELSE 0 END
    + CASE LOWER(d.non_eu_operations)          WHEN 'false' THEN -0.05086572354888771 WHEN 'true' THEN -0.17450094987563347 WHEN 'unknown' THEN 0.004903253255952854 ELSE 0 END
    + CASE LOWER(d.turnover_10m_to_500m_eur)   WHEN 'false' THEN -0.16150812880266724 WHEN 'true' THEN -0.09645440891765765 WHEN 'unknown' THEN -0.0449481513979897 ELSE 0 END
    + CASE LOWER(d.heavy_large_products)       WHEN 'false' THEN -0.050820388714084494 WHEN 'true' THEN -0.062310795252904845 WHEN 'unknown' THEN 0.025326354673188205 ELSE 0 END
    + CASE LOWER(d.operates_europe_wide)       WHEN 'false' THEN -0.1812178769217589 WHEN 'true' THEN 0.03169008753973013 WHEN 'unknown' THEN -0.05772174798582227 ELSE 0 END
    + CASE LOWER(d.manufactures_product)       WHEN 'false' THEN -0.09135988284829209 WHEN 'true' THEN -0.01578573170173398 WHEN 'unknown' THEN -0.28816673660538455 ELSE 0 END
    + CASE LOWER(d.mainly_b2c)                 WHEN 'false' THEN -0.030404572212813043 WHEN 'true' THEN -0.11933925103442233 WHEN 'unknown' THEN -0.09323862402918759 ELSE 0 END
    + CASE LOWER(d.high_quality_physical_goods) WHEN 'false' THEN -0.08407194863374717 WHEN 'true' THEN -0.024769104380562765 WHEN 'unknown' THEN -0.1443110899430542 ELSE 0 END
    + CASE LOWER(d.low_cost_consumer_products)  WHEN 'false' THEN -0.05565687419125419 WHEN 'true' THEN 0.05026151070673836 WHEN 'unknown' THEN -0.2820964795098649 WHEN 'partial' THEN -0.7191522565129611 ELSE 0 END

    -- ============================================================
    -- CATEGORICAL: online
    -- ============================================================
    + CASE LOWER(CAST(d.online AS STRING)) WHEN 'true' THEN -0.07541606842202789 WHEN 'false' THEN -0.5397222798605793 ELSE 0.1062734370313775 END

    -- ============================================================
    -- CATEGORICAL: payment_method
    -- ============================================================
    + CASE LOWER(d.payment_method)
        WHEN 'invoice' THEN -0.00000593473779407494
        WHEN 'creditcard' THEN -0.16222340897896984
        WHEN 'paypal' THEN 0.035444836044058126
        WHEN 'klarna' THEN -0.4204481799079659
        WHEN 'sofort' THEN -0.4204481799079659  -- mapped to klarna
        WHEN 'bancontact' THEN 0.32839560966525144
        WHEN 'ideal' THEN -0.1318001141983648
        WHEN 'advance_payment' THEN 0.041069443765247904
        WHEN 'advance_payment_wise' THEN 0.041069443765247904
        WHEN 'advancepayment' THEN 0.041069443765247904
        WHEN 'przelewy24' THEN -0.35585390151964036
        WHEN 'belfius' THEN -0.8998594267255149
        WHEN 'billie' THEN 0.046636753465026104
        WHEN 'trustly' THEN 0
        ELSE -0.35117487703131195  -- _null
      END

    -- ============================================================
    -- CATEGORICAL: transport_type_first_transport
    -- ============================================================
    + CASE LOWER(d.transport_type_first_transport)
        WHEN 'express_1200_kg' THEN -0.07164918243729212
        WHEN 'full_truck_24_t' THEN 0.07856094735676566
        ELSE 0.7314563562221194  -- _null
      END

    -- ============================================================
    -- CATEGORICAL: vehicle_type_first_transport
    -- ============================================================
    + CASE d.vehicle_type_first_transport
        WHEN 'Loading from above' THEN -1.0090647288605212
        WHEN 'Overhang' THEN -0.7455498019249021
        WHEN 'Small van' THEN -0.14500307813606342
        WHEN 'Tail lift and pallet truck' THEN -0.14619399492007565
        WHEN '3,2t Shipment' THEN -0.01934229068327046
        WHEN 'Dangerous Goods' THEN 0.009642811761652511
        WHEN '12t Shipment' THEN 0.018337507885265166
        WHEN 'Medium van' THEN 0.0459485798505546
        WHEN 'Width 230cm loading space' THEN 0.19575835527804575
        WHEN '2,4t Shipment' THEN 0.19739518683690896
        WHEN '24t Shipment' THEN 0.18550335110407606
        WHEN 'Width 220cm loading space' THEN 0.20939917092622387
        WHEN 'Large van' THEN 0.2721545098397925
        WHEN '5t Shipment' THEN 0.2785774636546063
        WHEN 'Length 480cm loading space' THEN 0.710275693059552
        WHEN 'Length 450cm loading space' THEN 0.9796427358149071
        WHEN 'Cooling-vehicle' THEN 1.5447771209066998
        ELSE 0.7314563562221194  -- _null
      END

    -- ============================================================
    -- CATEGORICAL: shipper_language
    -- ============================================================
    + CASE LOWER(d.shipper_language)
        WHEN 'cs' THEN -0.2364902016064497
        WHEN 'da' THEN -0.3346683179634214
        WHEN 'de' THEN 0.012438440538666032
        WHEN 'en' THEN 0.13408050154306417
        WHEN 'es' THEN -0.3452472562353442
        WHEN 'fr' THEN -0.18428981718833637
        WHEN 'it' THEN -0.06614715935468193
        WHEN 'nl' THEN -0.01332541076048741
        WHEN 'pl' THEN -0.20107492818628617
        ELSE 0.9685348059675722  -- _null
      END

    -- ============================================================
    -- CATEGORICAL: loading_country_code
    -- ============================================================
    + CASE UPPER(d.loading_country_code)
        WHEN 'AT' THEN 0.052630829955904554 WHEN 'BE' THEN 0.05735337090407901
        WHEN 'BG' THEN 0.33480260239603316  WHEN 'CH' THEN -0.3574806137560447
        WHEN 'CZ' THEN -0.3173167981151924  WHEN 'DE' THEN 0.04981692174870813
        WHEN 'DK' THEN -0.05756833928405996 WHEN 'EE' THEN 1.6664561937426199
        WHEN 'ES' THEN -0.2550982808619707  WHEN 'FI' THEN -1.1370994096132252
        WHEN 'FR' THEN -0.19737740227039333 WHEN 'GB' THEN -0.20068450228647428
        WHEN 'HR' THEN -0.9488181600180816  WHEN 'HU' THEN 1.7494432048512736
        WHEN 'IT' THEN -0.002189422835830118 WHEN 'LU' THEN 0.15605535818398883
        WHEN 'MC' THEN -0.6497010563227194  WHEN 'NL' THEN -0.012654741663777988
        WHEN 'PL' THEN -0.17030881838838308 WHEN 'PT' THEN -0.12912270582442836
        WHEN 'RO' THEN 1.6041755370842918   WHEN 'SE' THEN 0.13368900971362854
        WHEN 'SI' THEN -0.9384967242965124  WHEN 'SK' THEN 1.0830929558070248
        ELSE 0
      END

    -- ============================================================
    -- CATEGORICAL: unloading_country_code
    -- ============================================================
    + CASE UPPER(d.unloading_country_code)
        WHEN 'AT' THEN -0.0317014617214245  WHEN 'BE' THEN 0.05983985331793877
        WHEN 'BG' THEN -0.8486482795862077  WHEN 'CH' THEN -0.3767013435373036
        WHEN 'CZ' THEN 0.006202220511354719 WHEN 'DE' THEN 0.026212912128504465
        WHEN 'DK' THEN 0.11522243470303177  WHEN 'ES' THEN -0.23908724267652284
        WHEN 'FR' THEN -0.1794292913251229  WHEN 'GB' THEN -0.20158088851896402
        WHEN 'HR' THEN 0.3365195383612399   WHEN 'HU' THEN 0.7561582222746955
        WHEN 'IT' THEN 0.03336274722484016  WHEN 'LT' THEN 0.6462978594512653
        WHEN 'LU' THEN 0.0014041763048870046 WHEN 'LV' THEN -0.9061673375654165
        WHEN 'MC' THEN -0.8012708854025692  WHEN 'NL' THEN -0.004952206699566343
        WHEN 'PL' THEN 0.019005906981966757 WHEN 'PT' THEN -0.3127772784489193
        WHEN 'SE' THEN 0.44609934458403266  WHEN 'SI' THEN -0.21833161998479186
        WHEN 'SK' THEN 0.2652945915113065
        ELSE 0
      END

    -- ============================================================
    -- CATEGORICAL: TLD
    -- ============================================================
    + CASE LOWER(d.tld)
        WHEN '.aero' THEN 0.6502634152327026 WHEN '.ag' THEN 0.43231921896807124
        WHEN '.agency' THEN -0.43272025552234 WHEN '.ai' THEN -0.003480242253640681
        WHEN '.amsterdam' THEN 1.6635411026530031 WHEN '.app' THEN -0.9066106295913593
        WHEN '.ar' THEN -0.7750471250959377 WHEN '.archi' THEN -0.5841714708057819
        WHEN '.art' THEN 0.2000578279429108 WHEN '.at' THEN 0.011254480084047003
        WHEN '.be' THEN 0.0863372067517017 WHEN '.beer' THEN -0.7506684779687889
        WHEN '.berlin' THEN -0.7378980550621429 WHEN '.bg' THEN -0.5909244364668889
        WHEN '.bike' THEN 2.010964308814818 WHEN '.bio' THEN 0.1405543398750746
        WHEN '.biz' THEN 0.4677183633269249 WHEN '.business' THEN -0.6692947386942757
        WHEN '.ca' THEN 0.6907320111323177 WHEN '.care' THEN -0.9028522846729727
        WHEN '.cat' THEN -0.6400932794130567 WHEN '.cc' THEN -0.2565745110372459
        WHEN '.ch' THEN -0.5283264692305081 WHEN '.cloud' THEN 0.3962096117023705
        WHEN '.club' THEN -0.6893749533343131 WHEN '.cn' THEN -0.0009229268777407734
        WHEN '.co' THEN 0.20431015931105817 WHEN '.com' THEN -0.010379525113181135
        WHEN '.company' THEN -1.0451816899599393 WHEN '.coop' THEN -0.6194922106044662
        WHEN '.cy' THEN -1.0522807626814823 WHEN '.cz' THEN 0.0943210264503995
        WHEN '.de' THEN -0.014812343825890235 WHEN '.dev' THEN -0.6860838411964041
        WHEN '.digital' THEN 0.2833177654410286 WHEN '.dk' THEN -0.1794531384982014
        WHEN '.earth' THEN -0.864697217848788 WHEN '.edu' THEN -0.7194896096787968
        WHEN '.education' THEN 2.236703617326663 WHEN '.energy' THEN -0.7540372823712933
        WHEN '.es' THEN -0.4074533293966866 WHEN '.eu' THEN -0.0755346080155647
        WHEN '.events' THEN 1.9654708366935727 WHEN '.expert' THEN -0.7001807355738416
        WHEN '.financial' THEN -0.6887683089338323 WHEN '.fr' THEN -0.18171200489019243
        WHEN '.games' THEN -0.7432109768312829 WHEN '.gg' THEN 0.7445236290687979
        WHEN '.global' THEN -0.335049632708224 WHEN '.gmbh' THEN -0.38840974652938426
        WHEN '.group' THEN -0.09525267945323382 WHEN '.gy' THEN 2.080688866267988
        WHEN '.hamburg' THEN -1.1426608439385233 WHEN '.health' THEN 2.266421770939927
        WHEN '.healthcare' THEN -0.8013911108872812 WHEN '.hk' THEN 2.116574893875189
        WHEN '.house' THEN 0.3902667121450253 WHEN '.hr' THEN -1.102905004603688
        WHEN '.hu' THEN -0.9873772697158445 WHEN '.ie' THEN -0.6956249677120364
        WHEN '.il' THEN -0.8360650644053133 WHEN '.immo' THEN -0.6952253656488734
        WHEN '.immobilien' THEN -0.8849425235548725 WHEN '.inc' THEN -0.8739548579564496
        WHEN '.info' THEN -0.20881474904244846 WHEN '.international' THEN -0.950013394481779
        WHEN '.io' THEN -0.1035509052565893 WHEN '.it' THEN -0.1700182247197127
        WHEN '.jp' THEN -1.1067170123396066 WHEN '.kids' THEN -0.7874451645001229
        WHEN '.koeln' THEN 0.1503178082798481 WHEN '.kr' THEN -0.8424260420274503
        WHEN '.la' THEN -0.8751055197428415 WHEN '.land' THEN 2.2174524996750318
        WHEN '.law' THEN 1.1351007681882985 WHEN '.leclerc' THEN -0.7168124104430251
        WHEN '.legal' THEN -0.8169801115155572 WHEN '.life' THEN 1.1023738613580099
        WHEN '.lt' THEN -0.9141002834515117 WHEN '.lu' THEN 0.11793852900880152
        WHEN '.me' THEN 0.3604704572123422 WHEN '.media' THEN -0.8855566576466536
        WHEN '.moe' THEN -0.6606828879703097 WHEN '.ms' THEN -1.0032318088061456
        WHEN '.mt' THEN -0.9149326628033754 WHEN '.mu' THEN -0.6386508662976813
        WHEN '.museum' THEN -0.9810860397477745 WHEN '.net' THEN 0.015709660000029952
        WHEN '.network' THEN -0.9633327887837395 WHEN '.nl' THEN -0.09335686965367644
        WHEN '.nrw' THEN -0.852337666485662 WHEN '.nu' THEN 2.200693569777098
        WHEN '.one' THEN -0.9889606992959515 WHEN '.online' THEN 0.4673468705537943
        WHEN '.org' THEN -0.2113019316642931 WHEN '.ovh' THEN 2.190815711655396
        WHEN '.paris' THEN -0.08475658204024497 WHEN '.pl' THEN -0.19167977843929904
        WHEN '.plus' THEN 1.7319733799317678 WHEN '.pro' THEN 0.12391740234793644
        WHEN '.productions' THEN 1.8290781870735 WHEN '.pt' THEN -0.6882743760141289
        WHEN '.re' THEN -0.7577952550138694 WHEN '.ro' THEN -0.7782520757696013
        WHEN '.rocks' THEN 1.9244633348698574 WHEN '.schule' THEN -0.9657027394181049
        WHEN '.se' THEN -0.8600003156429166 WHEN '.sener' THEN -0.9466059998572675
        WHEN '.services' THEN 1.6628783927922006 WHEN '.sg' THEN -1.2047762744610424
        WHEN '.shop' THEN -0.6509377675601441 WHEN '.site' THEN 1.7888001856603253
        WHEN '.sk' THEN -0.9561200261167013 WHEN '.so' THEN -0.7410934618240594
        WHEN '.solutions' THEN 0.7827854883731726 WHEN '.space' THEN -0.8072676611248851
        WHEN '.store' THEN -0.3112813482352293 WHEN '.studio' THEN -0.1460479496218846
        WHEN '.support' THEN 1.851647914313975 WHEN '.systems' THEN 1.7958456954592816
        WHEN '.tax' THEN 0.612356903477952 WHEN '.team' THEN -0.6962709620072306
        WHEN '.tech' THEN 0.14310246195216092 WHEN '.tirol' THEN 0.14109729788592063
        WHEN '.tr' THEN -0.9818934915094663 WHEN '.tv' THEN -0.513953133495216
        WHEN '.uk' THEN -0.33012300882324114 WHEN '.us' THEN -0.8929793032651698
        WHEN '.vin' THEN -0.7668210829912783 WHEN '.vision' THEN -0.698272438322039
        WHEN '.work' THEN -0.7053453806108098 WHEN '.world' THEN 1.7042873397678695
        WHEN '.xyz' THEN -0.6027411024499743
        ELSE 0
      END

    AS z_score

  FROM `zipmend-2e643.ml.company_scoring_data_v4` d
  WHERE d.domain IS NOT NULL
)

SELECT
  domain,
  tld,
  -- Input features (for building test payloads)
  net_revenue_first_transport,
  distance_first_transport,
  transport_type_first_transport,
  vehicle_type_first_transport,
  online,
  payment_method,
  shipper_language,
  loading_country_code,
  unloading_country_code,
  -- Model outputs
  ROUND(1 / (1 + EXP(-z_score)), 6) AS probability,
  ROUND(LEAST(GREATEST(1 / (1 + EXP(-z_score)) * 3, 0.6), 2.4), 4) AS multiplier,
  CASE
    WHEN LEAST(GREATEST(1 / (1 + EXP(-z_score)) * 3, 0.6), 2.4) < 0.8 THEN 'b_kunden'
    WHEN LEAST(GREATEST(1 / (1 + EXP(-z_score)) * 3, 0.6), 2.4) < 1.2 + 0.000000001 THEN 'a_kunden'
    ELSE 'a_plus_kunden'
  END AS label,
  -- Example adjusted values
  ROUND(LEAST(GREATEST(1 / (1 + EXP(-z_score)) * 3, 0.6), 2.4) * net_revenue_first_transport, 2) AS adjusted_value,
  orders_total,
  min_3_orders
FROM model
ORDER BY probability DESC
